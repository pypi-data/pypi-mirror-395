!
! Copyright Intel Corporation.
! 
! This software and the related documents are Intel copyrighted materials, and
! your use of them is governed by the express license under which they were
! provided to you (License). Unless the License provides otherwise, you may
! not use, modify, copy, publish, distribute, disclose or transmit this
! software or the related documents without Intel's prior written permission.
! 
! This software and the related documents are provided as is, with no express
! or implied warranties, other than those that are expressly stated in the
! License.
!
! Copyright (C) by Argonne National Laboratory
! 
! 				  COPYRIGHT
! 
! The following is a notice of limited availability of the code, and disclaimer
! which must be included in the prologue of the code and in all source listings
! of the code.
! 
! Copyright Notice
! 1998--2020, Argonne National Laboratory
! 
! Permission is hereby granted to use, reproduce, prepare derivative works, and
! to redistribute to others.  This software was authored by:
! 
! Mathematics and Computer Science Division
! Argonne National Laboratory, Argonne IL 60439
! 
! (and)
! 
! Department of Computer Science
! University of Illinois at Urbana-Champaign
! 
! 
! 			      GOVERNMENT LICENSE
! 
! Portions of this material resulted from work developed under a U.S.
! Government Contract and are subject to the following license: the Government
! is granted for itself and others acting on its behalf a paid-up, nonexclusive,
! irrevocable worldwide license in this computer software to reproduce, prepare
! derivative works, and perform publicly and display publicly.
! 
! 				  DISCLAIMER
! 
! This computer code material was prepared, in part, as an account of work
! sponsored by an agency of the United States Government.  Neither the United
! States, nor the University of Chicago, nor any of their employees, makes any
! warranty express or implied, or assumes any legal liability or responsibility
! for the accuracy, completeness, or usefulness of any information, apparatus,
! product, or process disclosed, or represents that its use would not infringe
! privately owned rights.
! 
! 			   EXTERNAL CONTRIBUTIONS
! 
! Portions of this code have been contributed under the above license by:
! 
!  * Intel Corporation
!  * Cray
!  * IBM Corporation
!  * Microsoft Corporation
!  * Mellanox Technologies Ltd.
!  * DataDirect Networks.
!  * Oak Ridge National Laboratory
!  * Sun Microsystems, Lustre group
!  * Dolphin Interconnect Solutions Inc.
!  * Institut Polytechnique de Bordeaux
!
!     
!

!    user include file for Fortran MPI-IO programs 
!
      INTEGER MPI_MODE_RDONLY, MPI_MODE_RDWR, MPI_MODE_WRONLY
      INTEGER MPI_MODE_DELETE_ON_CLOSE, MPI_MODE_UNIQUE_OPEN
      INTEGER MPI_MODE_CREATE, MPI_MODE_EXCL
      INTEGER MPI_MODE_APPEND, MPI_MODE_SEQUENTIAL
      PARAMETER (MPI_MODE_RDONLY=2, MPI_MODE_RDWR=8, MPI_MODE_WRONLY=4)
      PARAMETER (MPI_MODE_CREATE=1, MPI_MODE_DELETE_ON_CLOSE=16)
      PARAMETER (MPI_MODE_UNIQUE_OPEN=32, MPI_MODE_EXCL=64)
      PARAMETER (MPI_MODE_APPEND=128, MPI_MODE_SEQUENTIAL=256)
!
      INTEGER MPI_FILE_NULL
      PARAMETER (MPI_FILE_NULL=0)
!
      INTEGER MPI_MAX_DATAREP_STRING
      PARAMETER (MPI_MAX_DATAREP_STRING=128)
!
      INTEGER MPI_SEEK_SET, MPI_SEEK_CUR, MPI_SEEK_END
      PARAMETER (MPI_SEEK_SET=600, MPI_SEEK_CUR=602, MPI_SEEK_END=604)
!
      INTEGER MPIO_REQUEST_NULL
      PARAMETER (MPIO_REQUEST_NULL=0)
!
      integer*8 MPI_DISPLACEMENT_CURRENT
      PARAMETER (MPI_DISPLACEMENT_CURRENT=-54278278)
!
      INTEGER MPI_OFFSET_KIND
      PARAMETER (MPI_OFFSET_KIND=           8)
!
!
!
!
!
!
!
!
!
!
!
!
!
