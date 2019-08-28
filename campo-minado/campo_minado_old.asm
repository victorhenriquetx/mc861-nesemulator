  .inesprg 1   ; 1x 16KB PRG code
  .ineschr 1   ; 1x  8KB CHR data
  .inesmap 0   ; mapper 0 = NROM, no bank swapping
  .inesmir 1   ; background mirroring
  

;;;;;;;;;;;;;;;

  .rsset $0000       ; put pointers in zero page
p_tiles_Lo  .rs 1   ; pointer variables are declared in RAM
p_tiles_Hi  .rs 1   ; low byte first, high byte immediately after

p_array_Lo  .rs 1   ; pointer variables are declared in RAM
p_array_Hi  .rs 1   ; low byte first, high byte immediately after



;;;;;;;;;;;;;;;
  .bank 0
  .org $C000 
RESET:
  SEI          ; disable IRQs
  CLD          ; disable decimal mode
  LDX #$40
  STX $4017    ; disable APU frame IRQ
  LDX #$FF
  TXS          ; Set up stack
  INX          ; now X = 0
  STX $2000    ; disable NMI
  STX $2001    ; disable rendering
  STX $4010    ; disable DMC IRQs

vblankwait1:       ; First wait for vblank to make sure PPU is ready
  BIT $2002
  BPL vblankwait1

clrmem:
  LDA #$00
  STA $0000, x
  STA $0100, x
  STA $0200, x
  STA $0400, x
  STA $0500, x
  STA $0600, x
  STA $0700, x
  LDA #$FE
  STA $0300, x
  INX
  BNE clrmem
   
vblankwait2:      ; Second wait for vblank, PPU is ready after this
  BIT $2002
  BPL vblankwait2


LoadPalettes:
  LDA $2002             ; read PPU status to reset the high/low latch
  LDA #$3F
  STA $2006             ; write the high byte of $3F00 address
  LDA #$00
  STA $2006             ; write the low byte of $3F00 address
  LDX #$00              ; start out at 0
LoadPalettesLoop:
  LDA palette, x        ; load data from address (palette + the value in x)
                          ; 1st time through loop it will load palette+0
                          ; 2nd time through loop it will load palette+1
                          ; 3rd time through loop it will load palette+2
                          ; etc
  STA $2007             ; write to PPU
  INX                   ; X = X + 1
  CPX #$20              ; Compare X to hex $10, decimal 16 - copying 16 bytes = 4 sprites
  BNE LoadPalettesLoop  ; Branch to LoadPalettesLoop if compare was Not Equal to zero
                        ; if compare was equal to 32, keep going down



LoadSprites:
  LDX #$00              ; start at 0
  LDY #$00
  
  LDA #$00
  STA $0050 ; i
  STA $0051 ; j

  LDA #$40
  STA $0052 ; horizontal
  STA $0053 ; vertical

  STA $0054 ; temp

  LDA #$00
  STA p_tiles_Lo
  LDA #$02
  STA p_tiles_Hi

  LDA #$00
  STA p_array_Lo
  LDA #$01
  STA p_array_Hi

  ; escrevendo dados
  LDA #$01
  STA $0100

  LDA #$03
  STA $0101

  LDA #$05
  STA $0102



; LoadSpritesLoop:


for_i:
  LDA #$40
  STA $0052
for_j:

  ; select position
  LDA $0053
  STA $0200, x        ; put sprite 0 in center ($40) of screen vert
  INX

  ; select tile
  LDA [p_array_Lo], y
  STA $0054
  INY
  AND #%00000001
  BEQ hidden

  LDA $0054
  LSR A
  JMP select_tile

hidden:
  LDA #$10

select_tile:
  STA $0200, x        ; tile number = 0
  INX
  
  ; select attr
  LDA #$00
  STA $0200, x        ; tile number = 0
  INX
  
  ; select position
  CLC
  LDA $0052
  ADC #$8
  STA $0200, x        ; put sprite 0 in center ($80) of screen horiz
  STA $0052
  INX
  
  
  
  INC $0051
  LDA $0051
  CMP #$8
  BNE for_j

  LDA #$00
  STA $0051
  
  CLC
  LDA $0053
  ADC #$08
  STA $0053
  
  CLC
  INC $0050
  LDA $0050
  CMP #$8
  BNE for_i






  ; LDA sprites, x        ; load data from address (sprites +  x)
  ; STA $0200, x          ; store into RAM address ($0200 + x)
  ; INX                   ; X = X + 1
  ; CPX #$20              ; Compare X to hex $20, decimal 32
  ; BNE LoadSpritesLoop   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
                        ; if compare was equal to 32, keep going down
              
              

  LDA #%10000000   ; enable NMI, sprites from Pattern Table 1
  STA $2000

  LDA #%00010000   ; enable sprites
  STA $2001

Forever:
  JMP Forever     ;jump back to Forever, infinite loop
  
 

NMI:
  LDA #$00
  STA $2003       ; set the low byte (00) of the RAM address
  LDA #$02
  STA $4014       ; set the high byte (02) of the RAM address, start the transfer


LatchController:
  LDA #$01
  STA $4016
  LDA #$00
  STA $4016       ; tell both the controllers to latch buttons


ReadA: 
  LDA $4016       ; player 1 - A
  AND #%00000001  ; only look at bit 0
  BEQ ReadADone   ; branch to ReadADone if button is NOT pressed (0)
                  ; add instructions here to do something when button IS pressed (1)
  LDA $0203       ; load sprite X position
  CLC             ; make sure the carry flag is clear
  ADC #$01        ; A = A + 1
  STA $0203       ; save sprite X position
ReadADone:        ; handling this button is done
  

ReadB: 
  LDA $4016       ; player 1 - B
  AND #%00000001  ; only look at bit 0
  BEQ ReadBDone   ; branch to ReadBDone if button is NOT pressed (0)
                  ; add instructions here to do something when button IS pressed (1)
  LDA $0203       ; load sprite X position
  SEC             ; make sure carry flag is set
  SBC #$01        ; A = A - 1
  STA $0203       ; save sprite X position
ReadBDone:        ; handling this button is done


  
  RTI             ; return from interrupt
 
;;;;;;;;;;;;;;  
  
  
  
  .bank 1
  .org $E000
palette:
  .db $06,$0F,$2A,$30,$30,$35,$36,$37,$38,$39,$3A,$3B,$3C,$3D,$3E,$0F
  .db $0F,$2A,$2D,$30,$31,$02,$38,$3C,$0F,$1C,$15,$14,$31,$02,$38,$3C

sprites:
     ;vert tile attr horiz
  .db $80, $10, $00, $70   ;sprite 0

  .org $FFFA     ;first of the three vectors starts here
  .dw NMI        ;when an NMI happens (once per frame if enabled) the 
                   ;processor will jump to the label NMI:
  .dw RESET      ;when the processor first turns on or is reset, it will jump
                   ;to the label RESET:
  .dw 0          ;external interrupt IRQ is not used in this tutorial
  
  
;;;;;;;;;;;;;;  
  
  
  .bank 2
  .org $0000
  .incbin "campo-minado.chr"   ;includes 8KB graphics file from SMB1