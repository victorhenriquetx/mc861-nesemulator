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


  LDA #%10000000   ; enable NMI, sprites from Pattern Table 1
  STA $2000

  LDA #%00010000   ; enable sprites
  STA $2001

Forever:
  JMP Forever     ;jump back to Forever, infinite loop
  
 

NMI:
  JSR printField

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

  JSR ReadController1  ;;get the current button data for player 1

  RTI             ; return from interrupt


printField:
  LDX #$00                ; "index/iterator" for sprites
  LDY #$03                ; every 4 loops, there will be a hex to convert to a sprite
                          ; starts at 3, because the first hex to convert is at loop #2
printFieldLoop:
  LDA sprites, x     ; reads next from field
  ;CPY #$04
  ;JSR decideSprite
  STA $0200, x
  INY                     ; y++
  INX                     ; x++
  CPX #$FF                ; field has 64 tiles (4 bytes each so 256 loops)
  BNE printFieldLoop
  ; 255 loops, there is one more left
  LDA sprites, x     ; reads last field
  STA $0200, x
  RTS                     ; TODO: should return or keep going?

decideSprite:
  AND #%10000000          ; check if value is visible
  BEQ hiddenSprite
  LDA sprites, x     ; if visible, decides which sprite to use
  AND #%00111111
  BEQ emptySprite
  CMP #$01
  BEQ oneSprite
  CMP #$02
  BEQ twoSprite
  CMP #$03
  BEQ threeSprite
  CMP #$04
  BEQ fourSprite
  CMP #$0A
  BEQ flagSprite
  CMP #$0B
  BEQ bombSprite

hiddenSprite:
  LDY #$01                  ; resets hex-sprite convertion counter
  LDA sprites, x
  AND #%01000000            ; checks if field is selected
  BNE hiddenSpriteSelected
  LDA #$10
  RTS
hiddenSpriteSelected:
  LDA #$12
  RTS

emptySprite:
  LDY #$01                  ; resets hex-sprite convertion counter
  LDA sprites, x
  AND #%01000000            ; checks if field is selected
  BNE emptySpriteSelected
  LDA #$04
  RTS
emptySpriteSelected:
  LDA #$04
  RTS

oneSprite:
  LDY #$01                  ; resets hex-sprite convertion counter
  LDA sprites, x
  AND #%01000000            ; checks if field is selected
  BNE oneSpriteSelected
  LDA #$00
  RTS
oneSpriteSelected:
  LDA #$21
  RTS

twoSprite:
  LDY #$01                  ; resets hex-sprite convertion counter
  LDA sprites, x
  AND #%01000000            ; checks if field is selected
  BNE twoSpriteSelected
  LDA #$01
  RTS
twoSpriteSelected:
  LDA #$22
  RTS

threeSprite:
  LDY #$01                  ; resets hex-sprite convertion counter
  LDA sprites, x
  AND #%01000000            ; checks if field is selected
  BNE threeSpriteSelected
  LDA #$02
  RTS
threeSpriteSelected:
  LDA #$23
  RTS

fourSprite:
  LDY #$01                  ; resets hex-sprite convertion counter
  LDA sprites, x
  AND #%01000000            ; checks if field is selected
  BNE fourSpriteSelected
  LDA #$03
  RTS
fourSpriteSelected:
  LDA #$30
  RTS

flagSprite:
  LDY #$01                  ; resets hex-sprite convertion counter
  LDA sprites, x
  AND #%01000000            ; checks if field is selected
  BNE flagSpriteSelected
  LDA #$11
  RTS
flagSpriteSelected:
  LDA #$20
  RTS

bombSprite:
  LDY #$01                ; resets hex-sprite convertion counter
  LDA #$13
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


Check_movement:
right:
  LDA buttons1
  AND #%00000001
  BEQ left

  LDX #$01
  STX button_pressed

  CLC
  LDA #$01
  STA p_array_Hi

  LDA tile_selected
  STA p_array_Lo

  LDX tile_selected
  LDY #$00
  LDA [p_array_Lo], y
  AND #%10111111
  STA $0100, x

  ;;;;;;;;;;;; PAREI AQUIIII - HAYASHIDA *************************************************
  ;;;;;;;;;;;;
  ;;;;;;;;;;;; PAREI AQUIIII - HAYASHIDA *************************************************
  ;;;;;;;;;;;;
  ;;;;;;;;;;;; PAREI AQUIIII - HAYASHIDA *************************************************
  ;;;;;;;;;;;;
  ;;;;;;;;;;;; PAREI AQUIIII - HAYASHIDA *************************************************
  ;;;;;;;;;;;;
  ;;;;;;;;;;;; PAREI AQUIIII - HAYASHIDA *************************************************
  ;;;;;;;;;;;;
  ;;;;;;;;;;;; PAREI AQUIIII - HAYASHIDA *************************************************
  ;;;;;;;;;;;;

  JMP end_movement
left:

down:

up:

start:

select:

b_button:

a_button:

end_movement
  RTS

;;;;;;;;;;;;;;  
  
  
  
  .bank 1
  .org $E000
palette:
  .db $06,$0F,$2A,$30,$30,$35,$36,$37,$38,$39,$3A,$3B,$3C,$3D,$3E,$0F
  .db $0F,$2A,$2D,$30,$31,$02,$38,$3C,$0F,$1C,$15,$14,$31,$02,$38,$3C

sprites:
     ;vert tile attr horiz
  .db $5C,$00,$00,$5C       ; row 1
  .db $5C,$00,$00,$64       ; y-position, hex value, attributes, x-position
  .db $5C,$01,$00,$6C       ; hex value is what we should manipulate to display the sprite
  .db $5C,$02,$00,$74 
  .db $5C,$0B,$00,$7C
  .db $5C,$01,$00,$84
  .db $5C,$00,$00,$8C
  .db $5C,$00,$00,$94

  .db $64,$00,$00,$5C       ; row 2
  .db $64,$01,$00,$64
  .db $64,$03,$00,$6C
  .db $64,$0B,$00,$74
  .db $64,$03,$00,$7C
  .db $64,$01,$00,$84
  .db $64,$01,$00,$8C
  .db $64,$01,$00,$94

  .db $6C,$01,$00,$5C       ; row 3
  .db $6C,$02,$00,$64
  .db $6C,$0B,$00,$6C
  .db $6C,$0B,$00,$74
  .db $6C,$02,$00,$7C
  .db $6C,$01,$00,$84
  .db $6C,$03,$00,$8C
  .db $6C,$0B,$00,$94

  .db $74,$0B,$00,$5C       ; row 4
  .db $74,$02,$00,$64
  .db $74,$02,$00,$6C
  .db $74,$02,$00,$74
  .db $74,$01,$00,$7C
  .db $74,$01,$00,$84
  .db $74,$0B,$00,$8C
  .db $74,$0B,$00,$94

  .db $7C,$01,$00,$5C       ; row 5
  .db $7C,$01,$00,$64
  .db $7C,$00,$00,$6C
  .db $7C,$00,$00,$74
  .db $7C,$00,$00,$7C
  .db $7C,$02,$00,$84
  .db $7C,$03,$00,$8C
  .db $7C,$03,$00,$94

  .db $84,$00,$00,$5C       ; row 6
  .db $84,$00,$00,$64
  .db $84,$00,$00,$6C
  .db $84,$00,$00,$74
  .db $84,$00,$00,$7C
  .db $84,$01,$00,$84
  .db $84,$0B,$00,$8C
  .db $84,$01,$00,$94

  .db $8C,$01,$00,$5C       ; row 7
  .db $8C,$01,$00,$64
  .db $8C,$00,$00,$6C
  .db $8C,$00,$00,$74
  .db $8C,$00,$00,$7C
  .db $8C,$01,$00,$84
  .db $8C,$01,$00,$8C
  .db $8C,$01,$00,$94

  .db $94,$0B,$00,$5C       ; row 8
  .db $94,$01,$00,$64
  .db $94,$00,$00,$6C
  .db $94,$00,$00,$74
  .db $94,$00,$00,$7C
  .db $94,$00,$00,$84
  .db $94,$00,$00,$8C
  .db $94,$00,$00,$94

;hex  sprite
;$00  1
;$01  2
;$02  3
;$03  4
;$04  empty (could also be any other one)
;$10  hidden
;$11  flag
;$12  selected hidden
;$13  bomb
;$20  selected flag
;$21  selected 1
;$22  selected 2
;$23  selected 3
;$30  selected 4

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