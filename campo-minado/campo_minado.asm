  .inesprg 1   ; 1x 16KB PRG code
  .ineschr 1   ; 1x  8KB CHR data
  .inesmap 0   ; mapper 0 = NROM, no bank swapping
  .inesmir 1   ; background mirroring
  

;;;;;;;;;;;;;;;

  .rsset $0000       ; put pointers in zero page

selected_tile .rs 1
button_a .rs 1
button_b .rs 1
button_up .rs 1
button_down .rs 1
button_left .rs 1
button_right .rs 1
button_select .rs 1
button_start .rs 1

sprites_hi .rs 1
sprites_lo .rs 1

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

  ; initial application state
  LDA #$01              ; selects initial tile (1,1)
  STA selected_tile     ; #$05 to select (2,1) and #$21 to select (1,2)

  LDA #$EE
  STA sprites_hi

  LDA #$00
  STA sprites_lo
  STA button_a          ; have all buttons start at previous value 0
  STA button_b
  STA button_up
  STA button_down
  STA button_left
  STA button_right
  STA button_select
  STA button_start

  JSR printField

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

  JSR readController
  RTI             ; return from interrupt

readController:
  LDA #$01
  STA $4016
  LDA #$00
  STA $4016       ; tell both the controllers to latch buttons

ReadA: 
  LDA $4016       ; player 1 - A
  AND #%00000001  ; only look at bit 0
  BEQ ReadADone   ; branch to ReadADone if button is NOT pressed (0)
                  ; add instructions here to do something when A is pressed (1)
  LDX selected_tile
  LDA sprites, x
  ORA #%01000000
  STA $0200, x

ReadADone:        ; handling this button is done

ReadB: 
  LDA $4016       ; player 1 - B
  AND #%00000001  ; only look at bit 0
  BEQ ReadBDone   ; branch to ReadBDone if button is NOT pressed (0)
                  ; add instructions here to do something when B is pressed (1)
ReadBDone:        ; handling this button is done

ReadSelect: 
  LDA $4016           ; player 1 - Select
  AND #%00000001      ; only look at bit 0
  BEQ ReadSelectDone  ; branch to ReadSelectDone if button is NOT pressed (0)
                      ; add instructions here to do something when SELECT is pressed (1)
ReadSelectDone:       ; handling this button is done

ReadStart: 
  LDA $4016           ; player 1 - Start
  AND #%00000001      ; only look at bit 0
  BEQ ReadStartDone   ; branch to ReadStartDone if button is NOT pressed (0)
                      ; add instructions here to do something when START is pressed (1)
ReadStartDone:        ; handling this button is done

ReadUp: 
  LDA $4016       ; player 1 - Up
  AND #%00000001  ; only look at bit 0
  CMP button_up   ; compares if it has changes from previous value (prevents button hold)
  BEQ ReadUpDone  ; branch to ReadUpDone if button is NOT pressed (0)
                  ; add instructions here to do something when UP is pressed (1)
  STA button_up   ; if it has changed, stores new value
  CMP #$00        ; if it has changed to 1, button has just been pressed
  BEQ ReadUpDone

  LDA selected_tile
  CMP #$20            ; checks if selected tile is at the top row of the field
  BMI ReadUpDone

  SBC #$20            ; if not, moves to previous position
  STA selected_tile

  LDX selected_tile
  LDA $0200, x        ; loads desired tile
  ORA #%01000000      ; sets to selected
  JSR pickSprite      ; picks sprite and saves it
  STA $0200, x
ReadUpDone:       ; handling this button is done

ReadDown: 
  LDA $4016           ; player 1 - Down
  AND #%00000001      ; only look at bit 0
  CMP button_down     ; compares if it has changes from previous value (prevents button hold)
  BEQ ReadDownDone    ; branch to ReadDownDone if button is NOT pressed (0)
                      ; add instructions here to do something when DOWN is pressed (1)
  STA button_down     ; if it has changed, stores new value
  CMP #$00            ; if it has changed to 1, button has just been pressed
  BEQ ReadDownDone

  LDA selected_tile
  CMP #$E0            ; checks if selected tile is at the bottom row of the field
  BMI ReadDownDone

  ADC #$20            ; if not, moves to previous position
  STA selected_tile

  LDX selected_tile
  LDA $0200, x        ; loads desired tile
  ORA #%01000000      ; sets to selected
  JSR pickSprite      ; picks sprite and saves it
  STA $0200, x
ReadDownDone:         ; handling this button is done

ReadLeft: 
  LDA $4016           ; player 1 - Left
  AND #%00000001      ; only look at bit 0
  CMP button_left     ; compares if it has changes from previous value (prevents button hold)
  BEQ ReadLeftDone    ; branch to ReadLeftDone if button is NOT pressed (0)
                      ; add instructions here to do something when LEFT is pressed (1)
  STA button_left     ; if it has changed, stores new value
  CMP #$00            ; if it has changed to 1, button has just been pressed
  BEQ ReadLeftDone

  LDA selected_tile
  CMP #$01            ; checks if selected tile is at the beginning of the field
  BMI ReadLeftDone

  SBC #$04            ; if not, moves to previous position
  STA selected_tile

  LDX selected_tile
  LDA $0200, x        ; loads desired tile
  ORA #%01000000      ; sets to selected
  JSR pickSprite      ; picks sprite and saves it
  STA $0200, x
ReadLeftDone:         ; handling this button is done

ReadRight: 
  LDA $4016           ; player 1 - Right
  AND #%00000001      ; only look at bit 0
  CMP button_right    ; compares if it has changes from previous value (prevents button hold)
  BEQ ReadRightDone   ; branch to ReadRightDone if button is NOT pressed (0)
                      ; add instructions here to do something when RIGHT is pressed (1)
  STA button_right    ; if it has changed, stores new value
  CMP #$00            ; if it has changed to 1, button has just been pressed
  BEQ ReadRightDone

  LDA selected_tile
  CMP #$FC            ; checks if selected tile is at the end of the field
  BMI ReadRightDone

  ADC #$04            ; if not, moves to next position
  STA selected_tile

  LDX selected_tile
  LDA $0200, x        ; loads desired tile
  ORA #%01000000      ; sets to selected
  JSR pickSprite      ; picks sprite and saves it
  STA $0200, x
ReadRightDone:        ; handling this button is done
  
  RTI             ; return from interrupt


printField:
  LDX #$00                ; "index/iterator" for sprites
  LDY #$03                ; every 4 loops, there will be a hex to convert to a sprite
                          ; starts at 3, because the first hex to convert is at loop #2
printFieldLoop:
  LDA sprites, x          ; reads next from field
  JSR checkSprite         ; chooses sprite, if necessary
  STA $0200, x
  INY                     ; y++
  INX                     ; x++
  CPX #$FF                ; field has 64 tiles (4 bytes each so 256 loops)
  BNE printFieldLoop
                          ; 255 loops so far, so last one is done manually
  LDA sprites, x          ; reads last field
  STA $0200, x
  RTS                     ; done printing field - returns to NMI treatment

checkSprite:
  CPY #$04                ; checks if should pick a sprite
  BEQ pickSprite
  RTS
pickSprite:
  AND #%10000000          ; check if value is visible
  BEQ hiddenSprite        ; if visibility bit is 0, use hidden sprite
  LDA sprites, x          ; if visible, loads hex value again
  AND #%00111111          ; get value only and decides which sprite to use
  BEQ emptySprite         ; if value is zero, use empty sprite
  CMP #$01                ; and keeps checking...
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
  LDY #$00                  ; resets hex-sprite convertion counter
  CPX selected_tile         ; checks if field is selected
  BEQ hiddenSpriteSelected
  LDA #$08
  RTS
hiddenSpriteSelected:
  LDA #$18
  RTS

emptySprite:
  LDY #$00                  ; resets hex-sprite convertion counter
  CPX selected_tile         ; checks if field is selected
  BEQ emptySpriteSelected
  LDA #$0B
  RTS
emptySpriteSelected:
  LDA #$1B
  RTS

oneSprite:
  LDY #$00                  ; resets hex-sprite convertion counter
  CPX selected_tile         ; checks if field is selected
  BEQ oneSpriteSelected
  LDA #$00
  RTS
oneSpriteSelected:
  LDA #$10
  RTS

twoSprite:
  LDY #$00                  ; resets hex-sprite convertion counter
  CPX selected_tile         ; checks if field is selected
  BEQ twoSpriteSelected
  LDA #$01
  RTS
twoSpriteSelected:
  LDA #$11
  RTS

threeSprite:
  LDY #$00                  ; resets hex-sprite convertion counter
  CPX selected_tile         ; checks if field is selected
  BEQ threeSpriteSelected
  LDA #$02
  RTS
threeSpriteSelected:
  LDA #$12
  RTS

fourSprite:
  LDY #$00                  ; resets hex-sprite convertion counter
  CPX selected_tile         ; checks if field is selected
  BEQ fourSpriteSelected
  LDA #$03
  RTS
fourSpriteSelected:
  LDA #$13
  RTS

flagSprite:
  LDY #$00                  ; resets hex-sprite convertion counter
  CPX selected_tile         ; checks if field is selected
  BEQ flagSpriteSelected
  LDA #$09
  RTS
flagSpriteSelected:
  LDA #$19
  RTS

bombSprite:
  LDY #$00                ; resets hex-sprite convertion counter
  LDA #$0A
  RTS


;;;;;;;;;;;;;;



  .bank 1
  .org $E000
palette:
  .db $0F,$01,$20,$10,$0F,$19,$20,$10,$0F,$06,$20,$10,$3C,$3D,$3E,$0F
  .db $0F,$01,$20,$10,$0F,$19,$20,$10,$0F,$06,$20,$10,$3C,$3D,$3E,$0F

sprites:
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
;$04  5
;$05  6
;$06  7
;$07  8
;$08  hidden
;$09  flag
;$0A  bomb
;$0B  empty
;$10  1 selected   
;$11  2 selected
;$12  3 selected
;$13  4 selected
;$14  5 selected
;$15  6 selected
;$16  7 selected
;$17  8 selected
;$18  hidden selected
;$19  flag selected

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
