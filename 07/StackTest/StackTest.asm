
//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_2
D;JEQ
D=0
@CEND_2
0;JMP
(TRUE_2)
D=-1
(CEND_2)
@SP
A=M-1
M=D

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_5
D;JEQ
D=0
@CEND_5
0;JMP
(TRUE_5)
D=-1
(CEND_5)
@SP
A=M-1
M=D

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_8
D;JEQ
D=0
@CEND_8
0;JMP
(TRUE_8)
D=-1
(CEND_8)
@SP
A=M-1
M=D

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_11
D;JLT
D=0
@CEND_11
0;JMP
(TRUE_11)
D=-1
(CEND_11)
@SP
A=M-1
M=D

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_14
D;JLT
D=0
@CEND_14
0;JMP
(TRUE_14)
D=-1
(CEND_14)
@SP
A=M-1
M=D

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_17
D;JLT
D=0
@CEND_17
0;JMP
(TRUE_17)
D=-1
(CEND_17)
@SP
A=M-1
M=D

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_20
D;JGT
D=0
@CEND_20
0;JMP
(TRUE_20)
D=-1
(CEND_20)
@SP
A=M-1
M=D

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_23
D;JGT
D=0
@CEND_23
0;JMP
(TRUE_23)
D=-1
(CEND_23)
@SP
A=M-1
M=D

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@TRUE_26
D;JGT
D=0
@CEND_26
0;JMP
(TRUE_26)
D=-1
(CEND_26)
@SP
A=M-1
M=D

//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

//push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

//neg
@SP
A=M-1
M=-M

//and
@SP
AM=M-1
D=M
A=A-1
M=D&M

//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

//or
@SP
AM=M-1
D=M
A=A-1
M=D|M

//not
@SP
A=M-1
M=!M
