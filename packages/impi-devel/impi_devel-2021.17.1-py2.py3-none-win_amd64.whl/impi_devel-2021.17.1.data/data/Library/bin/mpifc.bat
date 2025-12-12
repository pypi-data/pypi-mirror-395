@echo off & setlocal
rem Copyright Intel Corporation.
rem 
rem This software and the related documents are Intel copyrighted materials,
rem and your use of them is governed by the express license under which they
rem were provided to you (License). Unless the License provides otherwise,
rem you may not use, modify, copy, publish, distribute, disclose or transmit
rem this software or the related documents without Intel's prior written
rem permission.
rem 
rem This software and the related documents are provided as is, with no
rem express or implied warranties, other than those that are expressly stated
rem in the License.

rem ----------------------------------------------------------------------------
rem mpifc.bat
rem Simple script to compile and/or link MPI programs.
rem This script knows the default flags and libraries, and can handle
rem alternative FORTRAN compilers and the associated flags and libraries.
rem We assume that (a) the FORTRAN compiler can both compile and link programs
rem We use MPI_xxx so that the user may continue to use CFLAGS, LIBS, etc
rem to modify the behavior of the compiler and linker.
rem ----------------------------------------------------------------------------

rem Keep the self name (as "filename.ext") in the variable before cycle. We will use it later.
set selfname=%~nx0

rem MPIVERSION is the version of the Intel^(R^) MPI Library that mpifc is intended for
set MPIVERSION=2021.17

echo %selfname% for the Intel^(R^) MPI Library %MPIVERSION% for Windows*
echo Copyright Intel Corporation.
echo\

set fisrst_arg=x%1
set "fisrst_arg=%fisrst_arg:"=%"
set "fisrst_arg=%fisrst_arg:)=%"
if "%fisrst_arg%" == "x" (
    echo Simple script to compile and/or link MPI programs.
    echo This script knows the default flags and libraries, and can handle
    echo alternative Fortran compilers and the associated flags and libraries.
    echo Usage: "%~nx0 [options] <files>"
    echo ---------------------------------------------------------------------------- 
    echo The following options are supported:
    echo    -fc=^<name^>             to specify compiler name: i.e. -fc=ifort
    echo    -echo                  to print the scripts during its execution
    echo    -show                  to show command lines without real calling
    echo    -show_env              to show environment variables
    echo    -v                     to print version of the script
    echo    -ilp64                 to link ilp64 wrapper library
    echo    -no_ilp64              disable ilp64 support explicitly
    echo    -t or -trace
    echo                           to build with Intel^(R^) Trace Collector Library
    echo    -check_mpi             to build with the Intel^(R^) Trace Collector correctness
    echo                           checking library
    echo    -profile=^<name^>        to specify a profile configuration file in 
    echo                           the I_MPI_COMPILER_CONFIG_DIR folder: i.e. -profile=myprofile.conf
    echo    -link_mpi=^<name^>
    echo                    link against the specified version of the Intel^(R^) MPI Library
    echo                    i.e -link_mpi=opt^|dbg
    echo All other options will be passed to the compiler without changing.
    echo ---------------------------------------------------------------------------- 
    echo The following environment variables are used:
    echo    CMPLR_ROOT      Intel^(R^) Compiler installation directory path
    echo    I_MPI_ROOT      Intel^(R^) MPI Library installation directory path 
    echo    I_MPI_{FC,F77,F90} or MPICH_{FC,F77,F90}  
    echo                    the path/name of the underlying compiler to be used.
    echo    I_MPI_{FC,F77,F90}_PROFILE or MPI{FC,F77,F90}_PROFILE 
    echo                    name of profile file ^(without extension^) 
    echo    I_MPI_COMPILER_CONFIG_DIR 
    echo                    folder which contains configuration files *.conf
    echo    VT_ROOT         Intel^(R^) Trace Collector installation directory path
    echo ---------------------------------------------------------------------------- 
    exit /B 0
)

rem The CMPLR_ROOT should be defined by a installer
if "%CMPLR_ROOT%" == "" (
    echo You have to source ^<Intel Compiler^>\bin\vars.bat
    exit /B 1
)
rem The I_MPI_ROOT should be defined by a installer 
if "%I_MPI_ROOT%" == "" (
    echo You have to source ^<Intel MPI^>\bin\mpivars.bat
    exit /B 1
)
set "I_MPI_INCDIR=%I_MPI_ROOT%\include"
set "I_MPI_LIBDIR=%I_MPI_ROOT%\lib"
set "I_MPI_CFGDIR=%I_MPI_ROOT%\etc"
if exist "%I_MPI_ROOT%\lib\mpi\debug" (
    set "I_MPI_DBG_LIB_DIR=\lib\mpi\debug"
    set "I_MPI_RELEASE_LIB_DIR=\lib"
) else (
    set "I_MPI_DBG_LIB_DIR=\lib\debug"
    set "I_MPI_RELEASE_LIB_DIR=\lib\release"
)
:: The environment variables I_MPI_COMPILER_CONFIG_DIR may be used
:: to override directory where *.conf files are placed.
if NOT "%I_MPI_COMPILER_CONFIG_DIR%" == "" (
    set I_MPI_CFGDIR=%I_MPI_COMPILER_CONFIG_DIR%
)

:: The environment variables I_MPI_{FC,F77,F90} and MPICH_{FC,F77,F90} may 
:: be used to override the default choice (the FC has highest priority).
set FC="%CMPLR_ROOT%\bin\ifort.exe"
if NOT "%I_MPI_F77%" == "" (
    set FC=%I_MPI_F77%
) else if NOT "%MPICH_F77%" == "" (
    set FC=%MPICH_F77%
) 
if NOT "%I_MPI_F90%" == "" (
    set FC=%I_MPI_F90%
) else if NOT "%MPICH_F90%" == "" (
    set FC=%MPICH_F90%
) 
if NOT "%I_MPI_FC%" == "" (
    set FC=%I_MPI_FC%
) else if NOT "%MPICH_FC%" == "" (
    set FC=%MPICH_FC%
)

:: The environment variables I_MPI_{FC,F77,F90}_PROFILE and MPI{FC,F77,F90}_RPOFILE
:: may be used to select profile file.
set profConf=
if NOT "%I_MPI_F77_PROFILE%" == "" (
    set profConf=%I_MPI_F77_PROFILE%
) else if NOT "%MPIF77_PROFILE%" == "" (
    set profConf=%MPIF77_PROFILE%
)
if NOT "%I_MPI_F90_PROFILE%" == "" (
    set profConf=%I_MPI_F90_PROFILE%
) else if NOT "%MPIF90_PROFILE%" == "" (
    set profConf=%MPIF90_PROFILE%
)
if NOT "%I_MPI_FC_PROFILE%" == "" (
    set profConf=%I_MPI_FC_PROFILE%
) else if NOT "%MPIFC_PROFILE%" == "" (
    set profConf=%MPIFC_PROFILE%
)

:: Override default mpi library
set mpilib_override=
if NOT "%I_MPI_LINK%" == "" (
    mpilib_override=%I_MPI_LINK%
)

rem Default settings for compiler, flags, and libraries
rem set FCCPP=
rem Fortran 90 Compiler characteristics
set FCINC=-I

rem f90modinc specifies how to add a directory to the search path for modules.
rem Some compilers (Intel ifc version 5) do not support this concept, and 
rem instead need 
rem a specific list of files that contain module names and directories.
rem The FCMODINCSPEC is a more general approach that uses <dir> and <file>
rem for the directory and file respectively.
rem set FCMODINC=-I
rem set FCMODINCSPEC=
rem set FCEXT=f90

set I_MPI_CFLAGS=
set I_MPI_LDFLAGS=
set I_MPI_LIBNAME=impi
set I_MPI_OTHERLIBS=
set I_MPI_TRACE_PATH=
set OTHER_INCLUDE=
set OTHER_LIBPATH=
set VTTRACE_LIBS_START=
rem set PMPILIBNAME=pmpich
rem set NEEDSPLIB="no"

rem Internal variables
rem Show is set to echo to cause the compilation command to be echoed instead 
rem of executed.
set Show=call
set static_mpi=no
set static_log=no
set ilp64=no
set no_ilp64=
set case_trace=no
set trace_opt=no
set param_was_processed=
set PROFILE_INCPATHS=""
set PROFILE_PRELIB=""
set PROFILE_POSTLIB=""

rem ------------------------------------------------------------------------
rem Argument processing.
rem
rem Look through the arguments for arguments that indicate compile only.
rem If these are *not* found, add the library options

set linking=yes
set allargs=
set argt=
set paramt=
set qarg=
set qargt=
set link_arg_was_processed=
set link_args=

set args_for_processing=%*
set "args_for_processing=%args_for_processing:"=%"
:CONTINUE_LOOP
    set arg=%1
    set param=%2

    set qarg=%arg%
    set arg_tmp=x%arg%
    set param_tmp=x%param%
    set "arg_tmp=%arg_tmp:"=%"
    set "param_tmp=%param_tmp:"=%"
    if NOT "%arg_tmp%" == "x" (
        set "arg=%arg:"=%"
    )
    if NOT "%param_tmp%" == "x" (
        set "param=%param:"=%"
    )

    if "%arg:~0,2%" == "/D" goto LOOP_D
    if "%arg:~0,2%" == "-D" goto LOOP_D
    if "%arg:~0,2%" == "/Q" goto LOOP_D
    if "%arg:~0,2%" == "-Q" goto LOOP_D
    if "%arg:~0,7%" == "/define" goto LOOP_D
    if "%arg:~0,7%" == "-define" goto LOOP_D
    goto AFTER_LOOP_D
:LOOP_D
    set "args_for_processing=%args_for_processing:)=%"
    if "%args_for_processing:~0,1%" == "-" set args_for_processing=/%args_for_processing:~1%
    if NOT "%args_for_processing:~0,2%" == "/D" (
        if NOT "%args_for_processing:~0,7%" == "/define" (
            if NOT "%args_for_processing:~0,2%" == "/Q" (
                set args_for_processing=%args_for_processing:* =%
                if "%args_for_processing:* =%" == "%args_for_processing%" goto PARSING
                goto LOOP_D
            )
        )
    )
:PARSING
    FOR /F "tokens=1,2 delims= " %%G IN ("%args_for_processing%") DO (
        set argt=%%G
        set paramt=%%H
    )
    set qargt=%argt%
    set argt_tmp=%argt%x
    set paramt_tmp=%paramt%x
    if NOT "%argt_tmp:~0,1%" == "x" (
        set "argt=%argt:"=%"
    )
    if NOT "%paramt_tmp:~0,1%" == "x" (
        set "paramt=%paramt:"=%"
    )
    set argt=-%argt:~1%
    set allargs=%allargs% %argt%
:CYCLE
    FOR /F "tokens=1,* delims=,=" %%G IN ("%argt%") DO (
        set argt=%%H
        if NOT "x%argt%" == "x" shift
    )
    if "x%argt%" == "x" goto AFTER_CYCLE
    goto CYCLE
:AFTER_CYCLE
    set args_for_processing=%args_for_processing:* =%
    goto CONTINUE_LOOP
:AFTER_LOOP_D
    FOR /F "tokens=1,2 delims= " %%G IN ("%args_for_processing%") DO (
        set argt=%%G
        set paramt=%%H
    )
    set args_for_processing=%args_for_processing:* =%

    rem The argument can be started with '/' instead of '-'
    rem so we replace "/" symbol to "-" 
    if "%argt:~0,1%" == "/" set arg=-%argt:~1%

    rem Call subroutine with argument and param
    if NOT "%arg_tmp:~0,1%" == "x" (
        set "arg=%arg:)=^^)%"
    )
    if NOT "%param_tmp:~0,1%" == "x" (
        set "param=%param:)=^^)%"
    )
    call :PARSE_ONE_ARG %arg% %param%
    if ERRORLEVEL 3 exit /B 3

    if "%%2" == "" goto BREAK_LOOP
    shift
    if "%param_was_processed%" == "yes" (
        rem Remove the processed argument from the list
        shift
        set param_was_processed=
    ) 
    if %1.==. goto BREAK_LOOP

    goto CONTINUE_LOOP
:BREAK_LOOP

:: Override mpi library in regards to -link_mpi
    if "%mpilib_override%" == "opt" (
	    set MPILIBDIR=%I_MPI_RELEASE_LIB_DIR%
        set I_MPI_LIBNAME=impi
    ) else if "%mpilib_override%" == "dbg" (
	    set MPILIBDIR=%I_MPI_DBG_LIB_DIR%
        set I_MPI_LIBNAME=impi
    ) else if NOT "%mpilib_override%" == "" (
        echo Warning: incorrect library version specified. Automatically selected library will be used
    )

    if "%MPILIBDIR%" == "" (
        set MPILIBDIR=%I_MPI_RELEASE_LIB_DIR%
    )

rem If there is a file $I_MPI_CFGDIR/mpif90-$FCname.conf, 
rem where FCname is the name of the compiler with all spaces replaced by hyphens
rem (e.g., "f90 -64" becomes "f90--64", that file is sources, allowing other
rem changes to the compilation environment.  See the variables used by the 
rem script (defined above)
set FCname=%FC%
rem echo FCname="%FC%" 
if EXIST "%I_MPI_CFGDIR%\mpifc-%FCname%.conf" ( 
    call :CALL_CONF_FILE "%I_MPI_CFGDIR%\mpifc-%FCname%.conf"
)

if "%trace_opt%" == "yes" (
    if "%I_MPI_TRACE_PATH%" == "" (
        if "%static_log%" == "yes" (
            set "I_MPI_TRACE_PATH=%VT_LIB_DIR%"
        ) else (
            set "I_MPI_TRACE_PATH=%VT_SLIB_DIR%"
        )
    )
    set "VTTRACE_LIBS_START=%I_MPI_TRACE_PATH% %I_MPI_TRACE_LIB% %I_MPI_TRACE_EXTRA_LIB%"
)

rem Derived variables.  These are assembled from variables set from the
rem default, environment, configuration file (if any) and command-line
rem options (if any)
set mpilibs=%I_MPI_LIBNAME%.lib
rem if "%NEEDSPLIB%" == "yes" (
rem     set mpilibs=%PI_MPI_LIBNAME%.lib %mpilibs%
rem )

rem Handle the case of a profile switch
if NOT "%profConf%" == "" (
    if EXIST "%I_MPI_LIBDIR%\lib%profConf%.lib"   set profConfLibExists=yes
    if "%profConfLibExists%" == "yes" (
       set "mpilibs=%I_MPI_LIBDIR%\%profConf%.lib %mpilibs%"
    ) 
    if EXIST "%I_MPI_CFGDIR%\%profConf%.conf" (
        call :CALL_CONF_FILE "%I_MPI_CFGDIR%\%profConf%.conf"
    ) else (
        echo "The configuration file %I_MPI_CFGDIR%\%profConf%.conf is not found!"
    ) 
)

if "%ilp64%" == "yes" (
    set FCINCDIRS=%FCINC%"%I_MPI_INCDIR%\mpi\ilp64"  %FCINC%"%I_MPI_INCDIR%" %FCINC%"%I_MPI_INCDIR%\mpi"
    set "mpilibs=libmpi_ilp64.lib %mpilibs%"
) else (
    set FCINCDIRS=%FCINC%"%I_MPI_INCDIR%" %FCINC%"%I_MPI_INCDIR%\mpi"
)

if NOT %PROFILE_INCPATHS% == "" set I_MPI_CFLAGS=%PROFILE_INCPATHS% %I_MPI_CFLAGS%
if NOT %PROFILE_PRELIB% == ""   set mpilibs=%PROFILE_PRELIB% %mpilibs%
if NOT %PROFILE_POSTLIB% == ""  set mpilibs=%mpilibs% %PROFILE_POSTLIB%

rem rem Construct the line to add the include directory (not all compilers 
rem rem use -I, unfortunately)
rem if [ -z "${FCINC}" ] ; then
rem     rem If there is no path, add a link to the mpif.h file.
rem     rem There *must* be a way to provide the path the any modules (there
rem     rem may be too many to link)
rem     if [ ! -r mpif.h ] ; then
rem         remecho "Adding a symbolic link for mpif.h"
rem     trap "$Show /bin64/rm -f mpif.h" 0
rem     rem This should really be the (related) f77includedir (see mpif77).
rem     $Show ln -s ${includedir}/mpif.h mpif.h
rem     rem Remember to remove this file
rem     rmfiles="$rmfiles mpif.h"
rem     fi
rem     FCINCDIRS=
rem else
rem     rem Normally, FCINC is just -I, but some compilers have used different
rem     rem command line arguments
rem     set FCINCDIRS=%FCINC%%I_MPI_INCDIR%
rem fi

rem rem Handle the specification of the directory containing the modules
rem rem For now, these are in the includedir (no choice argument supported)
rem set moduledir=%modincdir%
rem set modulelib=%MPILIBNAME%f90
rem if [ -n "$FCMODINCSPEC" ] ; then
rem    newarg=`echo A"$FCMODINCSPEC" | \
rem     sed -e 's/^A//' -e 's%<dir>%'"$moduledir%g" -e 's/<file>/mpi/g'`
rem     FCMODDIRS="$newarg"
rem     FCMODLIBS="-l$modulelib"
rem elif [ -n "$FCMODINC" ] ; then
rem     FCMODDIRS="${FCMODINC}$moduledir"
rem     FCMODLIBS="-l$modulelib"
rem fi

rem A temporary statement to invoke the compiler
rem Place the -L before any args incase there are any mpi libraries in there.
rem Eventually, we'll want to move this after any non-MPI implementation 
rem libraries


if "%show_env%" == "yes" (
    call set | more
    exit /B 0
)

if "%linking%" == "yes" (
    if "%I_MPI_TRACE_PATH%" == "" (
    :: Place default mpi library at end for linking with ITAC
	%Show% %FC% %I_MPI_CFLAGS% %I_MPI_LDFLAGS% %allargs% %FCMODDIRS% %OTHER_INCLUDE% %FCINCDIRS% /link %OTHER_LIBPATH% /LIBPATH:"%I_MPI_ROOT%%MPILIBDIR%" /LIBPATH:"%I_MPI_LIBDIR%" %I_MPI_OTHERLIBS% %link_args% %mpilibs%
    ) else (
	%Show% %FC% %I_MPI_CFLAGS% %I_MPI_LDFLAGS% %allargs% %FCMODDIRS% %OTHER_INCLUDE% %FCINCDIRS% /link %OTHER_LIBPATH% /LIBPATH:"%I_MPI_TRACE_PATH%" /LIBPATH:"%I_MPI_ROOT%%MPILIBDIR%" /LIBPATH:"%I_MPI_LIBDIR%" %VTTRACE_LIBS_START% %mpilibs% %I_MPI_OTHERLIBS% %link_args%
    )
) else (
    %Show% %FC% %I_MPI_CFLAGS% %allargs% %FCMODDIRS% %OTHER_INCLUDE% %FCINCDIRS%
)

if ERRORLEVEL 1 (
    rem ERRORLEVEL >= 1
    echo ERROR in the compiling/linking [%ERRORLEVEL%]
    exit /B 3
)

rem if [ -n "$rmfiles" ] ; then
rem     for file in $rmfiles ; do
rem         objfile=`basename $file .f`
rem     if [ -s "${objfile}.o" ] ; then
rem         rem Rename 
rem         destfile=`echo $objfile | sed -e "s/.*$$-//"`
rem         mv -f ${objfile}.o ${destfile}.o
rem     fi
rem         rm -f $file
rem     done
rem     rm -f $rmfiles
rem fi

exit /B 0

rem This internal subroutine parses one  or two arguments(input parameters) 
rem and changes the aproriate variables
:PARSE_ONE_ARG
::    set arg=%1
    rem echo arg=%arg% 
::    set param=%2
    rem echo param=%param% 

    rem Set addarg to no if this arg should be ignored by the C compiler
    set addarg=yes
rem    set qarg=%arg%

    rem ----------------------------------------------------------------
    rem Start of case
    rem ----------------------------------------------------------------

    rem Only one -link must be present in the command line
    if "%link_arg_was_processed%" == "yes" (
        set link_args=%link_args% "%arg%"
        set addarg=no
        goto END_OF_CASE
    )
    if "%arg%" == "-link" (
        set link_arg_was_processed=yes
        set addarg=no
    )

    if "%arg:~0,2%" == "-I" (
        set OTHER_INCLUDE=%OTHER_INCLUDE% %qarg%
        set addarg=no
        goto END_OF_CASE
    )
    if "%arg:~0,8%" == "-LIBPATH" (
        set OTHER_LIBPATH=%qarg%
        set addarg=no
        goto END_OF_CASE
    )

    rem Fix bug with -D t="test"
    if NOT "%arg:~0,1%" == "-" goto END_OF_CASE

    if "%arg%" == "-show_env" set show_env=yes

    rem Compiler options that affect whether we are linking or no
    if "%arg%" == "-c"  set linking=no & goto END_OF_CASE
    if "%arg%" == "-S"  set linking=no & goto END_OF_CASE
    if "%arg%" == "-E"  set linking=no & goto END_OF_CASE
    rem if "%arg%" == "-M"  set linking=no & goto END_OF_CASE
    rem if "%arg%" == "-MM" set linking=no & goto END_OF_CASE

    if "%arg%" == "-echo" (
        set addarg=no
        echo on
        goto END_OF_CASE
    )  
rem    if "%arg:~0,4%" == "-fc=" ( rem "-fc=*"
rem        set FC=%arg:~4%
    rem Fix Tr#1754
    set _param=%param:(=^^(% 
    set _param=%_param:)=^^)%
    if "%arg%" == "-fc" ( rem "-fc=*"
        set FC=%_param: =%
        set addarg=no
        set param_was_processed=yes
        goto END_OF_CASE
    ) 
    if "%arg%" == "-link_mpi" ( rem "-link_mpi=*"
        set mpilib_override=%_param: =%
        set addarg=no
        set param_was_processed=yes
        goto END_OF_CASE
    )
    if "%arg%" == "-show" (
        set addarg=no
        set Show=call echo
        goto END_OF_CASE
    )

rem    if "%arg%" == "-config" ( 
rem        rem "-config=*"
rem        set addarg=no
rem        set FCname=%param%
rem        set param_was_processed=yes
rem        if EXIST %I_MPI_CFGDIR%/mpif90-%FCname%.conf 
rem            call %I_MPI_CFGDIR%/mpif90-%FCname%.conf
rem        else  
rem            echo "Configuration file mpif90-%FCname%.conf was not found."
rem        goto END_OF_CASE
rem    )

    if "%arg%" == "-compile-info" (
        set Show=call echo
        set addarg=no
        goto END_OF_CASE
    )
    rem -compile_info included for backward compatibility
    if "%arg%" == "-compile_info" (
        set Show=call echo
        set addarg=no
        goto END_OF_CASE
    )
    if "%arg%" == "-link-info" (
        set Show=call echo
        set addarg=no
        goto END_OF_CASE
    )
    rem -link_info included for backward compatibility
    if "%arg%" == "-link_info" (
        set Show=call echo
        set addarg=no
        goto END_OF_CASE
    )
    if "%arg%" == "-v" (
        set addarg=no
        exit /B 3
    )

    if "%arg:~0,8%" == "-profile" ( rem "-profile=*"
        rem Pass the name of a profiling configuration.  As
        rem a special case, lib<name>.so or lib<name>.a may be used
        rem if the library is in $I_MPI_LIBDIR
        if "%argt%" == "%arg%=%param%" set param_was_processed=yes
        set profConf="%param%"
        set addarg=no
        rem Loading the profConf file is handled below
        goto END_OF_CASE
    )

rem    if "%arg%" == "-mpe" ( rem "-mpe=*"
rem        rem Pass the name of a profiling configurationrem this is a special
rem        rem case for the MPE libs.  See -profile
rem        set profConf=%param%
rem        set param_was_processed=yes
rem        set profConf=mpe_%profConf%
rem        addarg=no
rem        rem Loading the profConf file is handled below
rem        goto END_OF_CASE
rem    )

    if "%arg%" == "-help" (
        rem The compiler help will be invoked
        goto END_OF_CASE
    )

    if "%arg%" == "-Z7" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-Zi" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-ZI" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-debug" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-debug:none" goto END_OF_CASE
    if "%arg%" == "-debug:extended" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-debug:semantic_stepping" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-debug:full" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-debug:partial" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE
    if "%arg%" == "-debug:minimal" set MPILIBDIR=%I_MPI_DBG_LIB_DIR%& goto END_OF_CASE

rem    if "%arg%" == "-static" (
rem        set static_mpi=yes
rem        set static_log=yes
rem        set addarg=yes
rem        goto END_OF_CASE
rem    )

    if "%arg%" == "-mt_mpi" (
        set addarg=no
        goto END_OF_CASE
    )

    if "%arg%" == "-ilp64" (
        set ilp64=yes
        set addarg=no
        goto END_OF_CASE
    )

    if "%arg%" == "-i8" (
        if "%no_ilp64%" == "" (
            set ilp64=yes
        )
        set addarg=yes
        goto END_OF_CASE
    )

    if "%arg%" == "-4I8" (
        if "%no_ilp64%" == "" (
            set ilp64=yes
        )
        set addarg=yes
        goto END_OF_CASE
    )

    if "%arg%" == "-integer_size:64" (
        if "%no_ilp64%" == "" (
            set ilp64=yes
        )
        set addarg=yes
        goto END_OF_CASE
    )

    if "%arg%" == "-no_ilp64" (
        set no_ilp64=yes
        set ilp64=no
        set addarg=no
        goto END_OF_CASE
    )

    if "%arg%" == "-t"       set case_trace=yes
    if "%arg%" == "-trace"   set case_trace=yes
    if "%case_trace%" == "yes" (
        if NOT DEFINED VT_ROOT (
            echo "You need to set VT_ROOT env variable to use -trace option"
            exit /B 3
        )
        if "%VT_LIB_DIR%" == "" (
            if "%VT_SLIB_DIR%" == "" (
                echo "You have to source <ITAC>\bin\itacvars.bat <mpi> to use -trace option"
                exit /B 3
            )
        )
        set I_MPI_TRACE_LIB=VT.lib
        set I_MPI_TRACE_EXTRA_LIB=%VT_ADD_LIBS%
        set I_MPI_CFLAGS=%I_MPI_CFLAGS% -I "%VT_ROOT%\include"
        set trace_opt=yes
        set addarg=no
        if "%param%" == "log" (
            set MPILIBDIR=\log
            set param_was_processed=yes
        )
        set case_trace=no
        goto END_OF_CASE
    )
    if "%arg%" == "-check_mpi" (
        if NOT DEFINED VT_ROOT (
            echo "You need to set VT_ROOT env variable to use -check_mpi option"
            exit /B 3
        )
        if "%VT_LIB_DIR%" == "" (
            if "%VT_SLIB_DIR%" == "" (
                echo "You have to source <ITAC>\bin\itacvars.bat <mpi> to use -check_mpi option"
                exit /B 3
            )
        )
        set I_MPI_TRACE_LIB=VTmc.lib
        set I_MPI_TRACE_EXTRA_LIB=%VT_ADD_LIBS%
        set I_MPI_CFLAGS=%I_MPI_CFLAGS% -I"%VT_ROOT%\include"
        set trace_opt=yes
        set addarg=no
        goto END_OF_CASE
    )

rem     *.F|*.F90|.fpp|.FPP)
rem rem If FCCPP is not empty, then we need to do the following:
rem rem    If any input files have the .F or .FC extension, then    
rem rem        If FCCPP = false, then
rem rem            generate an error message and exit
rem rem        Use FCCPP to convert the file from .F to .f, using 
rem rem            $TMPDIR/f$$-$count.f as the output file name
rem rem            Replace the input file with this name in the args
rem rem This is needed only for very broken systems
rem rem     
rem     if [ -n "$FCCPP" ] ; then
rem         if [ "$FCCPP" = "false" ] ; then
rem             echo "This Fortran compiler does not accept .F or .FC files"
rem         exit /B 1
rem         fi
rem         addarg=no
rem     rem Remove and directory names and extension
rem     $ext=`expr "$arg" : '.*\(\..*\)'`
rem         bfile=`basename $arg $ext`
rem     rem 
rem     TMPDIR=${TMPDIR:-/tmp}
rem     rem Make sure that we use a valid extension for the temp file.
rem         tmpfile=$TMPDIR/f$$-$bfile.$FCEXT
rem         if $FCCPP $cppflags $arg > $tmpfile ; then
rem             rem Add this file to the commandline list
rem         count=`expr $count + 1`
rem         allargs="$allargs $tmpfile"
rem         rmfiles="$rmfiles $tmpfile"
rem         else
rem         echo "Aborting compilation because of failure in preprocessing step"
rem         echo "for file $arg ."
rem         exit /B 1
rem         fi
rem     fi
rem     rem Otherwise, just accept the argument

    :END_OF_CASE
    rem ----------------------------------------------------------------
    rem end of case
    rem ----------------------------------------------------------------

    if "%addarg%" == "yes" (
        set allargs=%allargs% %qarg%
    )

GOTO :eof rem "GOTO :eof" will return to the position where you used CALL. 

:: Function for applying configuration file 
:CALL_CONF_FILE
    set conffile=%1
    set "conffile=%conffile:"=%"
    set conffile="%conffile%"
rem    set "conffile=%conffile:)=^)%"
    FOR /F "usebackq tokens=*" %%G IN (%conffile%) DO call %%G
    )
GOTO :eof  
