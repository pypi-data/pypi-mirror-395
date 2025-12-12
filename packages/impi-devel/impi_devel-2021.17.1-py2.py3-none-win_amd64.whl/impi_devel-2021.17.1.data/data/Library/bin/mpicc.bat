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
rem mpicc.bat
rem Simple script to compile and/or link MPI programs.
rem This script knows the default flags and libraries, and can handle
rem alternative C/C++ compilers and the associated flags and libraries.
rem 
rem We assume that (a) the C/C++ compiler can both compile and link programs
rem We use MPI_xxx so that the user may continue to use CFLAGS, LIBS, etc
rem to modify the behavior of the compiler and linker.
rem ----------------------------------------------------------------------------

rem Keep the self name (as "filename.ext") in the variable before cycle. We will use it later.
set selfname=%~nx0

rem MPIVERSION is the version of the Intel^(R^) MPI Library that mpicc is intended for
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
    echo alternative C compilers and the associated flags and libraries.
    echo Usage: "%~nx0 [options] <files>"
    echo ---------------------------------------------------------------------------- 
    echo The following options are supported:
    echo    -cc=^<name^>      to specify a C compiler name: i.e. -cc=icl.exe
    echo    -cxx=^<name^>     to specify a C++ compiler name: i.e. -cxx=icpc.exe
    echo    -echo           to print the scripts during its execution
    echo    -show           to show command lines without real calling
    echo    -show_env       to show environment variables
    echo    -v              to print version of the script
    echo    -ilp64          to link ilp64 wrapper library
    echo    -t or -trace
    echo                    to build with the Intel^(R^) Trace Collector Library
    echo    -check_mpi      to build with the Intel^(R^) Trace Collector correctness 
    echo                    checking library
    echo    -profile=^<name^> to specify a profile configuration file in 
    echo                    the I_MPI_COMPILER_CONFIG_DIR folder: i.e. -profile=myprofile
    echo    -link_mpi=^<name^>
    echo                    link against the specified version of the Intel^(R^) MPI Library
    echo                    i.e -link_mpi=opt^|dbg
    echo All other options will be passed to the compiler without changing.
    echo ---------------------------------------------------------------------------- 
    echo The following environment variables are used:
    echo    I_MPI_ROOT      Intel^(R^) MPI Library installation directory path 
    echo    I_MPI_{CC,CXX} or MPICH_{CC,CXX}  
    echo                    the path/name of the underlying compiler to be used
    echo    I_MPI_{CC,CXX}_PROFILE or MPI_{CC,CXX}_PROFILE 
    echo                    name of profile file ^(without extension^) 
    echo    I_MPI_COMPILER_CONFIG_DIR 
    echo                    folder which contains configuration files *.conf
    echo    VT_ROOT         Intel^(R^) Trace Collector installation directory path
    echo ---------------------------------------------------------------------------- 
    exit /B 0
)

rem The I_MPI_ROOT should be defined by a installer 
if "%I_MPI_ROOT%" == "" (
    echo You have to source ^<Intel MPI^>\etc\mpi\vars.bat
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

:: The default compiler is cl.exe. Here we get the full path to cl.exe
:: to avoid a binary hijacking vulnerability. To do that we use vswhere
:: if available, otherwise the VcToolsInstallDir env var.
set CC=
set CCname="cl.exe"
set InstallDir=
set Version=
set VsWhere="C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
if exist "%VsWhere%" (
    setlocal EnableDelayedExpansion
    for /f "usebackq tokens=*" %%i in (`%VsWhere% -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do (
        set InstallDir=%%i
    )
    if NOT "%I_MPI_MSVC_VERSION%" == "" (
        set Version=%I_MPI_MSVC_VERSION%
    ) else if exist "%InstallDir%\VC\Auxiliary\Build\Microsoft.VCToolsVersion.default.txt" (
        set /p Version=<"%InstallDir%\VC\Auxiliary\Build\Microsoft.VCToolsVersion.default.txt"
        set Version=!Version: =!
    )
    set CC="%InstallDir%\VC\Tools\MSVC\%Version%\bin\HostX64\x64\cl.exe"
    set CCname="cl.exe"
    setlocal DisableDelayedExpansion
) else (
    set CC="%VCToolsInstallDir%\bin\Hostx64\x64\cl.exe"
    set CCname="cl.exe"
)

:: The environment variables I_MPI_{CC,CXX} and MPICH_{CC,CXX} may
:: be used to override the default choice (the CC has highest priority).
if NOT "%I_MPI_CC%" == "" (
    set CC=%I_MPI_CC%
    set CCname=%CC%
) else if NOT "%MPICH_CC%" == "" (
    set CC=%MPICH_CC%
    set CCname=%CC%
)
if NOT "%I_MPI_CXX%" == "" (
    set CC=%I_MPI_CXX%
    set CCname=%CC%
) else if NOT "%MPICH_CXX%" == "" (
    set CC=%MPICH_CXX%
    set CCname=%CC%
)

:: The environment variables I_MPI_{CC,CXX}_PROFILE and MPI{CC,CXX}_RPOFILE
:: may be used to select profile file.
set profConf=
if NOT "%I_MPI_CC_PROFILE%" == "" (
    set profConf=%I_MPI_CC_PROFILE%
) else if NOT "%MPICC_PROFILE%" == "" (
    set profConf=%MPICC_PROFILE%
)
if NOT "%I_MPI_CXX_PROFILE%" == "" (
    set profConf=%I_MPI_CXX_PROFILE%
) else if NOT "%MPICXX_PROFILE%" == "" (
    set profConf=%MPICXX_PROFILE%
)

:: Override default mpi library
set mpilib_override=
if NOT "%I_MPI_LINK%" == "" (
    set mpilib_override=%I_MPI_LINK%
)

rem Default settings for compiler, flags, and libraries.
set I_MPI_CFLAGS=
set I_MPI_LDFLAGS=
set I_MPI_LIBNAME=impi
set I_MPI_OTHERLIBS=
set I_MPI_TRACE_PATH=
set OTHER_INCLUDE=
set OTHER_LIBPATH=
set VTTRACE_LIBS_START=
rem set NEEDSPLIB=no
rem set PI_MPI_LIBNAME=

rem Internal variables
rem Show is set to echo to cause the compilation command to be echoed instead 
rem of executed.
set Show=call
set static_mpi=no
set static_log=no
set ilp64=no
set case_trace=no
set trace_opt=no
set param_was_processed=
set PROFILE_INCPATHS=""
set PROFILE_PRELIB=""
set PROFILE_POSTLIB=""
rem icxp specific variables
set USE_ICPX=no
set LIB_PREFIX=
set LINKER_OPTION=/link

rem ------------------------------------------------------------------------
rem Argument processing.
rem 
rem Look through the arguments for arguments that indicate compile only.
rem If these are *not* found, add the library options

set linking=yes
set allargs=
set argt=
set paramt=
set link_arg_was_processed=
set link_args=

set args_for_processing=%*
set "args_for_processing=%args_for_processing:"=%"
:CONTINUE_LOOP
    set arg=%1
    set param=%2

    if %1.==. goto BREAK_LOOP

    rem Fix bug with IMB test (ignore "" parameters)
    if [%arg%] == [""] (
        shift 
        goto CONTINUE_LOOP    
    )

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
    if "%arg:~0,2%" == "/Q" goto CHECK_QOPTION
    if "%arg:~0,2%" == "-Q" goto CHECK_QOPTION
    goto AFTER_LOOP_D
:: Enable PARSE_ONE_ARG for Qoption
:CHECK_QOPTION
    if "%arg:~1%" == "Qopenmp" goto AFTER_LOOP_D
    if "%arg:~1%" == "Qparallel" goto AFTER_LOOP_D
:LOOP_D
    set "args_for_processing=%args_for_processing:)=%"
    if "%args_for_processing:~0,1%" == "-" set args_for_processing=/%args_for_processing:~1%
    if NOT "%args_for_processing:~0,2%" == "/D" (
        if NOT "%args_for_processing:~0,2%" == "/Q" (
            set args_for_processing=%args_for_processing:* =%
            if "%args_for_processing:* =%" == "%args_for_processing%" goto PARSING
            goto LOOP_D
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
    if "%arg:~0,1%" == "/" set arg=-%arg:~1%

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

rem If there is a file $I_MPI_CFGDIR/mpicc-$CCname.conf, 
rem where CCname is the name of the compiler with all spaces replaced by hyphens
rem (e.g., "cc -64" becomes "cc--64", that file is sources, allowing other
rem changes to the compilation environment.  See the variables used by the 
rem script (defined above)
rem echo CCname=%CCname%
if EXIST "%I_MPI_CFGDIR%\mpicc-%CCname%.conf" (
    call :CALL_CONF_FILE "%I_MPI_CFGDIR%\mpicc-%CCname%.conf"
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

set "mpilibs=%LIB_PREFIX%%I_MPI_LIBNAME%.lib"
if "%need_cxx_lib%" == "yes" (
    set "mpilibs=%mpilibs% %LIB_PREFIX%%I_MPI_LIBNAME%cxx.lib"
)

rem if "%NEEDSPLIB%" == "yes" (
rem     set mpilibs=%PI_MPI_LIBNAME%.lib %mpilibs%
rem )

rem Handle the case of a profile switch
if NOT "%profConf%" == "" (
    if EXIST "%I_MPI_LIBDIR%\%profConf%.lib" (
        set profConfLibExists=yes
    )
    if EXIST "%I_MPI_CFGDIR%\%profConf%.conf" (
        set profConfFileExists=yes
    )
)
if "%profConfLibExists%" == "yes" (
   set "mpilibs=%profConf%.lib %mpilibs%"
) else if NOT "%profConf%" == "" (
    if "%profConfFileExists%" == "yes" (
        call :CALL_CONF_FILE "%I_MPI_CFGDIR%\%profConf%.conf"
    ) else (
        echo "The configuration file %I_MPI_CFGDIR%\%profConf%.conf is not found!"
    )
)
if NOT %PROFILE_INCPATHS% == "" set I_MPI_CFLAGS=%PROFILE_INCPATHS% %I_MPI_CFLAGS%
if NOT %PROFILE_PRELIB% == ""   set mpilibs=%PROFILE_PRELIB% %mpilibs%
if NOT %PROFILE_POSTLIB% == ""  set mpilibs=%mpilibs% %PROFILE_POSTLIB%

if "%ilp64%" == "yes" (
   set mpilibs=libmpi_ilp64.lib %mpilibs%
)

rem A temporary statement to invoke the compiler
rem Place the -L before any args incase there are any mpi libraries in there.
rem Eventually, we'll want to move this after any non-MPI implementation 
rem libraries.
rem We use a single invocation of the compiler.  This will be adequate until
rem we run into a system that uses a separate linking command.  With any luck,
rem such archaic systems are no longer with us.  This also lets us
rem accept any argument; we don't need to know if we've seen a source
rem file or an object file.  Instead, we just check for an option that
rem suppressing linking, such as -c or -M.

if "%show_env%" == "yes" (
    call set | more
    exit /B 0
)

if "%linking%" == "yes" (
    if "%I_MPI_TRACE_PATH%" == "" (
        :: Place default mpi library at end for linking with ITAC
        %Show% %CC% %I_MPI_CFLAGS% %I_MPI_LDFLAGS% %allargs% %OTHER_INCLUDE% -I"%I_MPI_INCDIR%"  -I"%I_MPI_INCDIR%\mpi" %LINKER_OPTION% %OTHER_LIBPATH% /LIBPATH:"%I_MPI_ROOT%%MPILIBDIR%" /LIBPATH:"%I_MPI_LIBDIR%" %I_MPI_OTHERLIBS% %link_args% %mpilibs% 
    ) else (
        %Show% %CC% %I_MPI_CFLAGS% %I_MPI_LDFLAGS% %allargs% %OTHER_INCLUDE% -I"%I_MPI_INCDIR%"  -I"%I_MPI_INCDIR%\mpi" %LINKER_OPTION% %OTHER_LIBPATH% /LIBPATH:"%I_MPI_TRACE_PATH%" /LIBPATH:"%I_MPI_ROOT%%MPILIBDIR%" /LIBPATH:"%I_MPI_LIBDIR%" %VTTRACE_LIBS_START% %mpilibs% %I_MPI_OTHERLIBS% %link_args%
    )
) else (
    %Show% %CC% %I_MPI_CFLAGS% %allargs% %OTHER_INCLUDE% -I"%I_MPI_INCDIR%"
)

if ERRORLEVEL 1 (
    rem ERRORLEVEL >= 1
    echo ERROR in the compiling/linking [%ERRORLEVEL%]
    exit /B 3
)

exit /B 0


rem -------------------------------------------------------------------------
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
    if "%arg%" == "-QM"  set linking=no & goto END_OF_CASE
    if "%arg%" == "-QMM" set linking=no & goto END_OF_CASE

    rem ----------------------------------------------------------------
    rem Options that control how we use mpicc (e.g., -show, etc.) 
    if "%arg%" == "-echo" (
        set addarg=no
        echo on
        goto END_OF_CASE
    )  
rem    if "%arg:~0,4%" == "-cc=" ( rem "-cc=*"
rem        set CC=%arg:~4%
    rem Fix Tr#1754
    set _param=%param:(=^^(% 
    set _param=%_param:)=^^)%
    rem -cc=* -config=*
    if "%arg%" == "-cc" ( rem "-cc=*"
        set CC=%_param: =%
        set CCname=%CC%
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
    rem -cxx=* -config=*
    if "%arg%" == "-cxx" ( rem "-cxx=*"
        set CC=%_param: =%
        set CCname=%CC%
        set addarg=no
        set param_was_processed=yes
        set need_cxx_lib=yes
        if "%_param: =%" == "icpx" (
            set USE_ICPX=yes
            set LIB_PREFIX=/l
            set LINKER_OPTION=
        )
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
rem        set CCname=%param%
rem        set param_was_processed=yes
rem        if EXIST %I_MPI_CFGDIR%/mpicc-%CCname%.conf 
rem            call %I_MPI_CFGDIR%/mpicc-%CCname%.conf
rem        else  
rem            echo "Configuration file mpicc-%CCname%.conf was not found."
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
    
    if "%arg%" == "-mt_mpi" (
        set addarg=no
        goto END_OF_CASE
    )
    if "%arg%" == "-ilp64" (
        set ilp64=yes
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
        set I_MPI_CFLAGS=%I_MPI_CFLAGS% -I"%VT_ROOT%\include"
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
GOTO :eof  
