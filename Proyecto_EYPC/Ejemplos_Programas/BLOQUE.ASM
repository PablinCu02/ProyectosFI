   LD IX, 200
   LD A, 48H
   LD (IX+0),A
   LD A, 4fH
   LD (IX+1),A
   LD A, 4cH
   LD (IX+2),A
   LD A, 41H
   LD (IX+3),A
   LD A, 43H
   LD (IX+5),A
   LD A, 4fH
   LD (IX+6),A
   LD A, 4dH
   LD (IX+7),A
   LD A, 4fH
   LD (IX+8),A
   LD A, 45H
   LD (IX+10),A
   LD A, 53H
   LD (IX+11),A
   LD A, 54H
   LD (IX+12),A
   LD A, 41H
   LD (IX+13),A
   LD A, 53H
   LD (IX+14),A
   
 
   LD IY, 205
   PUSH IY
   LD C,5
   LD B, 9
   LD IY, 200
   
   
eti1:
   DEC IX
   DEC C
   LD A,C
   CP 0
   JP NZ,eti1
   PUSH IX

eti2:
   LD A,(IY+0)
   LD (IX+0),A
   INC IY
   INC IX
   DEC B
   LD A,B
   CP 0
   JP NZ, eti2
   
   POP IX
   POP IY
   LD C,5

eti3:
   LD A,(IX+0)
   LD (IY+0), A
   INC IY
   INC IX
   DEC C
   LD A,C
   CP 0
   JP NZ,eti3


   HALT
