// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	@2
	M=0	  // M[2] = 0 
(LOOP)
	@0 	  	
	D=M		// D = M[0]
	@END	
	D;JLE
	@1
	D=M 	// D = M[1]
	@2
	M=D+M	// M[2] += D
	@0 
	M=M-1	// M[0]--
	@LOOP
	0;JMP
(END)
	@END
	0;JMP