module mod_io

  ! Provides input/output procedures.

  use iso_fortran_env, only: int32, real32

  implicit none

  private
  public :: write_field

contains

  subroutine write_field(field, fieldname, time)
    ! Writes a field into a binary file.
    real(PRECISION_), intent(in) :: field(:,:)
    character(len=*), intent(in) :: fieldname
    integer(int32), intent(in) :: time
    integer(int32) :: fileunit, record_length
    character(len=100) :: filename, timestr, precision_str

    write(precision_str, '(i0)') sizeof(field(1,1))
    write(timestr, '(i4.4)') time

    filename = 'real'//trim(precision_str)//'/'//fieldname // '_' // trim(timestr) // '.dat'
    open(newunit=fileunit, file=filename)
    write(fileunit,*) field
    close(fileunit)
  end subroutine write_field

end module mod_io
