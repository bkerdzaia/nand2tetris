@261
D=A
@SP
M=D
@Sys.init
0;JMP
(CYCLE_START)
@R14
D=M
@R15
A=M
D;JLE
D=0
@SP
AM=M+1
A=A-1
M=D
@R14
M=M-1
@CYCLE_START
0;JMP
(Sys.init)
@JUMP_Sys.init
D=A
@R15
M=D
@0
D=A
@R14
M=D
@CYCLE_START
0;JMP
(JUMP_Sys.init)
@Sys.main_RETURN_ADDRESS
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys.main_RETURN_ADDRESS)
@SP
AM=M-1
D=M
@6
M=D
(Sys.init$LOOP)
@Sys.init$LOOP
0;JMP
(Sys.main)
@JUMP_Sys.main
D=A
@R15
M=D
@0
D=A
@R14
M=D
@CYCLE_START
0;JMP
(JUMP_Sys.main)
@123
D=A
@SP
AM=M+1
A=A-1
M=D
@Sys.add12_RETURN_ADDRESS
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.add12_RETURN_ADDRESS)
@SP
AM=M-1
D=M
@5
M=D
@246
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@R13
M=D
@R13
D=M
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.add12)
@JUMP_Sys.add12
D=A
@R15
M=D
@3
D=A
@R14
M=D
@CYCLE_START
0;JMP
(JUMP_Sys.add12)
@2
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
@12
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
AM=M+1
@LCL
D=M
@R13
M=D
@R13
D=M
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
