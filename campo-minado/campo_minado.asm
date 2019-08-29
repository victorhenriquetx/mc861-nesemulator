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

buttons1   .rs 1  ; player 1 gamepad buttons, one bit per button

tile_selected .rs 1
button_pressed .rs 1

tile_value .rs 1
move      .rs 1
key       .rs 1

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
  LDA $2000             ; read PPU status to reset the high/low latch
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


  LDA #%10000000   ; enable NMI, sprites from Pattern Table 1
  STA $2000

  LDA #%00010000   ; enable sprites
  STA $2001

  LDA #$01
  STA tile_selected

  LDA #$01
  STA move

    ; escrevendo dados
  LDA #$00
  STA $0100

  LDA #%01000010
  STA $0101

  LDA #$04
  STA $0102
  

  
  JSR print_field
Forever:
  JMP Forever     ;jump back to Forever, infinite loop
  
 

NMI:
  

  LDA #$00
  STA $2003       ; set the low byte (00) of the RAM address
  LDA #$02
  STA $4014       ; set the high byte (02) of the RAM address, start the transfer


  LDA #%10010000   ; enable NMI, sprites from Pattern Table 0, background from Pattern Table 1
  STA $2000
  LDA #%00011110   ; enable sprites, enable background, no clipping on left side
  STA $2001
  LDA #$00        ;;tell the ppu there is no background scrolling
  STA $2005
  STA $2005

  JSR ReadController1

  LDA move
  CMP #$05
  BNE button_release
  JSR Check_movement  ;;get the current button data for player 1
  JMP button_done

button_release:
  JSR Check_release
  
button_done:
  JSR print_field

  RTI             ; return from interrupt


print_field:
  LDX #$00              ; start at 0
  LDY #$00
  
  LDA #$00
  STA $0050 ; i
  STA $0051 ; j

  LDA #$40
  STA $0052 ; horizontal
  STA $0053 ; vertical

  LDA #$00
  STA p_tiles_Lo
  LDA #$02
  STA p_tiles_Hi

  LDA #$00
  STA p_array_Lo
  LDA #$01
  STA p_array_Hi

for_i:
  LDA #$40
  STA $0052
for_j:

  ; select position
  LDA $0053
  STA $0200, x        ; put sprite 0 in center ($40) of screen vert
  INX

  ; select tile  - Falta colocar condição de tile selected
  LDA [p_array_Lo], y
  INY
  STA tile_value
  AND #%01000000
  BEQ is_not_selected

  LDA tile_value
  AND #%10001111        ; clean selected bit
  ORA #%00010000        ; insert boarder
  STA tile_value

is_not_selected:
  AND #%10000000
  BEQ hidden

  LDA tile_value
  AND #%00011111
  JMP select_tile

hidden:
  LDA tile_value
  AND #%00010000
  ORA #%00001000


select_tile:
  STA $0200, x        ; tile number = 0
  INX
  
  ; select attr
  LDA #$0
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
  RTS

ReadController1:
  LDA #$01
  STA $4016
  LDA #$00
  STA $4016
  LDX #$08
ReadController1Loop:
  LDA $4016
  LSR A            ; bit0 -> Carry
  ROL buttons1     ; bit0 <- Carry
  DEX
  BNE ReadController1Loop
  RTS


Check_release:  
  LDA buttons1
  AND #%00001111            ; not selected
  BEQ end_release
  INC move
end_release:
  RTS

Check_movement:
  
right:
  LDA buttons1
  AND #%00000001            ; not selected
  BEQ left

  ; deselect tile
  LDA #$01
  STA p_array_Hi
  LDA tile_selected
  STA p_array_Lo

  LDA tile_selected
  AND #%00000111            ; invalid movement
  EOR #%00000111
  BEQ end_movement

  LDX tile_selected
  LDY #$00
  LDA [p_array_Lo], y
  AND #%10111111            ; zero -> bit 6
  STA $0100, x

  INC tile_selected
  LDA #$01
  STA p_array_Hi
  LDA tile_selected
  STA p_array_Lo

  
  LDX p_array_Lo
  LDY #$00
  LDA [p_array_Lo], y
  ORA #%01000000            ; one -> bit 6
  STA $0100, x

  LDA #$00
  STA move
  LDA #$01
  STA key

  JMP end_movement
left:
  LDA buttons1
  AND #%00000010            ; not selected
  BEQ down

  ; deselect tile
  LDA #$01
  STA p_array_Hi
  LDA tile_selected
  STA p_array_Lo

  LDA tile_selected
  AND #%00000111            ; invalid movement
  BEQ end_movement

  LDX tile_selected
  LDY #$00
  LDA [p_array_Lo], y
  AND #%10111111            ; zero -> bit 6
  STA $0100, x

  DEC tile_selected
  LDA #$01
  STA p_array_Hi
  LDA tile_selected
  STA p_array_Lo

  
  LDX p_array_Lo
  LDY #$00
  LDA [p_array_Lo], y
  ORA #%01000000            ; one -> bit 6
  STA $0100, x

  LDA #$00
  STA move
  LDA #$02
  STA key

  JMP end_movement
down:

end_movement:
  RTS

;;;;;;;;;;;;;;  
  
  
  
  .bank 1
  .org $E000
palette:
  .db $0F,$01,$20,$10,$0F,$19,$20,$10,$0F,$06,$20,$10,$3C,$3D,$3E,$0F
  .db $0F,$01,$20,$10,$0F,$19,$20,$10,$0F,$06,$20,$10,$3C,$3D,$3E,$0F

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
  .incbin "campo-minado2.chr"   ;includes 8KB graphics file from SMB1