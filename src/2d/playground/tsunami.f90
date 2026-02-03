program tsunami

  ! Tsunami simulator.
  !
  ! Solves the non-linear 2-d shallow water equation system:
  !
  !     du/dt + u du/dx + v du/dy + g dh/dx = 0
  !     dv/dt + u dv/dx + v dv/dy + g dh/dy = 0
  !     dh/dt + d(hu)/dx + d(hv)/dy = 0
  !
  ! This version is parallelized, and uses derived types.

  use iso_fortran_env, only: int32, real32, real64
  use mod_field32, only: Field32, diffx32=>diffx, diffy32=>diffy
  use mod_field64, only: Field64, diffx64=>diffx, diffy64=>diffy

  implicit none

  integer(int32) :: n

  integer(int32), parameter :: im = 30 ! grid size in x
  integer(int32), parameter :: jm = 30 ! grid size in y
  integer(int32), parameter :: num_time_steps = 3000 ! number of time steps
  integer(int32), parameter :: correct_interval = 100

  real(real32), parameter :: dt32 = 0.02 ! time step [s]
  real(real32), parameter :: dx32 = 1 ! grid spacing [m]
  real(real32), parameter :: dy32 = 1 ! grid spacing [m]
  real(real32), parameter :: g32 = 9.8 ! gravitational acceleration [m/s]

  real(real64), parameter :: dt64 = 0.02 ! time step [s]
  real(real64), parameter :: dx64 = 1 ! grid spacing [m]
  real(real64), parameter :: dy64 = 1 ! grid spacing [m]
  real(real64), parameter :: g64 = 9.8 ! gravitational acceleration [m/s]

  integer(int32), parameter :: ic = im/2, jc = jm/2
  
  real(real32), parameter :: decay32 = 0.02
  real(real64), parameter :: decay64 = 0.02

  type(Field32) :: h32, u32, v32, hm32
  type(Field64) :: h64, u64, v64, hm64

  type(Field32) :: du_x32, du_y32, dv_x32, dv_y32, dh_x32, dh_y32
  type(Field64) :: du_x64, du_y64, dv_x64, dv_y64, dh_x64, dh_y64
  
  if (this_image() == 1) print *, 'Tsunami started'

  call u32 % init('u', [im, jm])
  call v32 % init('v', [im, jm])
  call h32 % init('h', [im, jm])
  call hm32 % init('hm', [im, jm])

  call u64 % init('u', [im, jm])
  call v64 % init('v', [im, jm])
  call h64 % init('h', [im, jm])
  call hm64 % init('hm', [im, jm])

  call du_x32 % init('du_x', [im, jm])
  call du_y32 % init('du_y', [im, jm])
  call dv_x32 % init('dv_x', [im, jm])
  call dv_y32 % init('dv_y', [im, jm])
  call dh_x32 % init('dh_x', [im, jm])
  call dh_y32 % init('dh_y', [im, jm])

  call du_x64 % init('du_x', [im, jm])
  call du_y64 % init('du_y', [im, jm])
  call dv_x64 % init('dv_x', [im, jm])
  call dv_y64 % init('dv_y', [im, jm])
  call dh_x64 % init('dh_x', [im, jm])
  call dh_y64 % init('dh_y', [im, jm])
      
  ! initialize a gaussian blob in the center
  call h32 % set_gaussian(decay32, ic, jc)
  call h32 % sync_edges()

  call h64 % set_gaussian(decay64, ic, jc)
  call h64 % sync_edges()

  ! set mean water depth
  hm32 = real(10., real32)
  hm64 = real(10., real64)

  call h32 % write(0)
  call u32 % write(0)
  call v32 % write(0)

  call h64 % write(0)
  call u64 % write(0)
  call v64 % write(0)

  call du_x32 % write(0)
  call du_y32 % write(0)
  call dv_x32 % write(0)
  call dv_y32 % write(0)
  call dh_x32 % write(0)
  call dh_y32 % write(0)

  call du_x64 % write(0)
  call du_y64 % write(0)
  call dv_x64 % write(0)
  call dv_y64 % write(0)
  call dh_x64 % write(0)
  call dh_y64 % write(0)

  time_loop: do n = 1, num_time_steps

    if(mod(n,100) == 0) then
      print *, 'Computing time step', n, '/', num_time_steps!,  &
    end if

    du_x32 = diffx32(u32)/dx32
    du_y32 = diffy32(u32)/dy32
    du_x64 = diffx64(u64)/dx64
    du_y64 = diffy64(u64)/dy64

    dv_x32 = diffx32(v32)/dx32
    dv_y32 = diffy32(v32)/dy32
    dv_x64 = diffx64(v64)/dx64
    dv_y64 = diffy64(v64)/dy64

    ! compute u at next time step    
    u32 = u32 - (u32 * diffx32(u32) / dx32 + v32 * diffy32(u32) / dy32 &
         + g32 * diffx32(h32) / dx32) * dt32
    call u32 % sync_edges()
    
    u64 = u64 - (u64 * diffx64(u64) / dx64 + v64 * diffy64(u64) / dy64 &
         + g64 * diffx64(h64) / dx64) * dt64
    call u64 % sync_edges()

    ! compute v at next time step
    v32 = v32 - (u32 * diffx32(v32) / dx32 + v32 * diffy32(v32) / dy32 & 
         + g32 * diffy32(h32) / dy32) * dt32
    call v32 % sync_edges()

    v64 = v64 - (u64 * diffx64(v64) / dx64 + v64 * diffy64(v64) / dy64 &
         + g64 * diffy64(h64) / dy64) * dt64
    call v64 % sync_edges()

    ! compute h at next time step
    h32 = h32 - (diffx32(u32 * (hm32 + h32)) / dx32 + diffy32(v32 * (hm32 + h32)) / dy32) * dt32
    call h32 % sync_edges()

    h64 = h64 - (diffx64(u64 * (hm64 + h64)) / dx64 + diffy64(v64 * (hm64 + h64)) / dy64) * dt64
    call h64 % sync_edges()

    call h32 % write(n)
    call u32 % write(n)
    call v32 % write(n)

    call h64 % write(n)
    call u64 % write(n)
    call v64 % write(n)

    call du_x32 % write(n)
    call du_y32 % write(n)
    call dv_x32 % write(n)
    call dv_y32 % write(n)
    call dh_x32 % write(n)
    call dh_y32 % write(n)

    call du_x64 % write(n)
    call du_y64 % write(n)
    call dv_x64 % write(n)
    call dv_y64 % write(n)
    call dh_x64 % write(n)
    call dh_y64 % write(n)    

  end do time_loop

end program tsunami
