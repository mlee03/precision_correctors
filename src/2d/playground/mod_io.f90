module mod_io

  ! Provides input/output procedures.

  use iso_fortran_env, only: int32, real32, real64

  implicit none

  private
  public :: write_field

  interface write_field
     module procedure write_field32
     module procedure write_field64
  end interface write_field

contains

  subroutine write_field32(field, fieldname, time)
    ! Writes a field into a binary file.
    real(real32), intent(in) :: field(:,:)
    character(len=*), intent(in) :: fieldname
    integer(int32), intent(in) :: time
    integer(int32) :: fileunit, record_length
    character(len=100) :: filename, timestr, precision_str

    write(precision_str, '(i0)') sizeof(field(1,1))
    write(timestr, '(i5.5)') time

    filename = 'real4/'//fieldname // '_' // trim(timestr) // '.dat'
    open(newunit=fileunit, file=filename)
    write(fileunit,*) field
    close(fileunit)
  end subroutine write_field32

  subroutine write_field64(field, fieldname, time)
    ! Writes a field into a binary file.
    real(real64), intent(in) :: field(:,:)
    character(len=*), intent(in) :: fieldname
    integer(int32), intent(in) :: time
    integer(int32) :: fileunit, record_length
    character(len=100) :: filename, timestr, precision_str

    write(precision_str, '(i0)') sizeof(field(1,1))
    write(timestr, '(i5.5)') time

    filename = 'real8/'//fieldname // '_' // trim(timestr) // '.dat'
    open(newunit=fileunit, file=filename)
    write(fileunit,*) field
    close(fileunit)
  end subroutine write_field64
  
end module mod_io
