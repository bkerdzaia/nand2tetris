@256
D=A
@SP
M=D
@SimpleFunction.test
0;JMP
@CYCLE_END
0;JMP
(CYCLE_START)
@R14
D=M
@R15
A=M
D;JLE
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@R14
M=M-1
@CYCLE_START
0;JMP
(CYCLE_END)
(SimpleFunction.test)
@JUMP_SimpleFunction.test
D=A
@R15
M=D
@2
D=A
@R14
M=D
@CYCLE_START
0;JMP
(JUMP_SimpleFunction.test)
@1
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
@1
D=M
@1
A=D+A
D=M
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
@SP
AM=M-1
M=!M
@SP
AM=M+1
@2
D=M
@0
A=D+A
D=M
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
@2
D=M
@1
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
AM=M+1
@LCL
D=M
@R5
M=D
@R5
D=M
@5
A=D-A
D=M
@R6
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
@R5
D=M
@1
A=D-A
D=M
@THAT
M=D
@R5
D=M
@2
A=D-A
D=M
@THIS
M=D
@R5
D=M
@3
A=D-A
D=M
@ARG
M=D
@R5
D=M
@4
A=D-A
D=M
@LCL
M=D
@R6
A=M
0;JMP