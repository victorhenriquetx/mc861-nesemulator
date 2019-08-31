  .inesprg 1   ; 1x 16KB PRG code
  .ineschr 1   ; 1x  8KB CHR data
  .inesmap 0   ; mapper 0 = NROM, no bank swapping
  .inesmir 1   ; background mirroring
  

;;;;;;;;;;;;;;;

  .rsset $0000       ; put pointers in zero page
p_tiles_Lo  .rs 1   ; pointer variables are declared in RAM
p_tiles_Hi  .rs 1   ; low byte first, high byte immediately after

tile_selected .rs 1
tile_value .rs 1

temp      .rs 1
temp_2    .rs 1

var_i     .rs 1
var_j     .rs 1

bombs     .rs 1

button_a .rs 1
button_b .rs 1
button_up .rs 1
button_down .rs 1
button_left .rs 1
button_right .rs 1
button_select .rs 1
button_start .rs 1

queue .rs 64
array .rs 64

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



  LDA #$00
  STA tile_selected


  LDA #$00
  STA button_a          ; have all buttons start at previous value 0
  STA button_b
  STA button_up
  STA button_down
  STA button_left
  STA button_right
  STA button_select
  STA button_start
  
  LDX #$00
load_map_ram:
  LDA field, x
  STA array, x
  INX
  CPX #$40
  BNE load_map_ram
  
  LDA #$00
  STA bombs

  LDA #$80
  STA $0200        ;put sprite 0 in center ($80) of screen vertically
  LDA #$0A
  STA $0201        ;tile number = 0
  LDA #$00
  STA $0202        ;color palette = 0, no flipping
  LDA #$80
  STA $0203        ;put sprite 0 in center ($80) of screen horizontally
  
  ; select the first tile
  LDY #$00
  LDA array, y 
  ORA #$40
  STA array, y

  JSR print_field

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


  LDA #%10010000   ; enable NMI, sprites from Pattern Table 0, background from Pattern Table 1
  STA $2000
  LDA #%00011110   ; enable sprites, enable background, no clipping on left side
  STA $2001
  LDA #$00        ;;tell the ppu there is no background scrolling
  STA $2005
  STA $2005

  JSR ReadController

  ; LDA click
  
button_done:
  JSR print_field

  RTI             ; return from interrupt


print_field:
  LDX #$00              ; start at 0
  LDY #$00
  
  LDA #$00
  STA var_i ; i
  STA var_j ; j

  LDA #$40
  STA temp ; horizontal
  STA temp_2 ; vertical

  LDA #$00
  STA p_tiles_Lo
  LDA #$02
  STA p_tiles_Hi

  ; LDA #$00
  ; STA p_array_Lo
  ; LDA #$01
  ; STA p_array_Hi

for_i:
  LDA #$40
  STA temp
for_j:

  ; select position
  LDA temp_2
  STA $0200, x        ; put sprite 0 in center ($40) of screen vert
  INX
  ; select tile
  LDA array, y
  INY
  STA tile_value
  AND #%01000000
  BEQ is_not_selected

  LDA tile_value
  AND #%10111111        ; clean selected bit
  ORA #%00010000        ; insert boarder
  STA tile_value

is_not_selected:
  LDA tile_value
  AND #%10000000
  BEQ hidden

  LDA tile_value
  AND #%00011111
  JMP select_tile

hidden:
  LDA tile_value
  AND #%00100000
  BNE flag

  LDA tile_value
  AND #%00010000
  ORA #$09
  JMP select_tile
flag:
  LDA tile_value
  AND #%00010000
  ORA #$0A

select_tile:
  STA $0200, x        ; tile number = 0
  INX
  
  ; select attr
  LDA #$0
  STA $0200, x        ; tile number = 0
  INX
  
  ; select position
  CLC
  LDA temp
  ADC #$8
  STA $0200, x        ; put sprite 0 in center ($80) of screen horiz
  STA temp
  INX
  
  INC var_j
  LDA var_j
  CMP #$8
  BNE for_j

  LDA #$00
  STA var_j
  
  CLC
  LDA temp_2
  ADC #$08
  STA temp_2
  
  CLC
  INC var_i
  LDA var_i
  CMP #$8
  BEQ end_print
  JMP for_i
end_print:
  RTS

; check_release:  
;   LDA buttons1
;   AND #%11001111            ; not selected
;   BEQ end_release
;   INC click
; end_release:
;   RTS



ReadController:
  LDA #$01
  STA $4016
  LDA #$00
  STA $4016
  
ReadA:
  LDA $4016       ; player 1 - A
  AND #%00000001
  CMP button_a
  BEQ ReadB

  STA button_a
  CMP #$00
  BEQ ReadADone

  LDX tile_selected
  LDA array, x
  AND #%00100000
  BNE ReadADone

  ; disable bombs select
  LDA array, x
  AND #$0F
  CMP #$0B
  BNE continue

  JSR gameover
  BRK
continue:

  ; LDA array, x
  ; ORA #$80
  ; STA array, x

  ; LDA array, x
  JSR setNeighborsVisib

ReadADone:
ReadB:
  LDA $4016       ; player 1 - B
  AND #%00000001
  CMP button_b
  BEQ ReadBDone

  STA button_b
  CMP #$00
  BEQ ReadBDone

  LDX tile_selected

  LDA array, x
  STA temp
  AND #%00100000
  ADC #%00100000
  AND #%00100000
  STA temp_2

  AND #%00100000
  BEQ decrement_flags
  INC bombs
  JMP draw_flag
decrement_flags:
  DEC bombs
draw_flag:
  LDA temp
  AND #%11011111
  ORA temp_2
  STA array, x
ReadBDone:

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
  CMP button_up
  BEQ ReadUpDone

  STA button_up
  CMP #$00
  BEQ ReadUpDone

  ; deselect tile
  LDA tile_selected
  AND #%11111000            ; invalid movement
  BEQ ReadUpDone

  LDX tile_selected
  LDY #$00
  LDA array, x
  AND #%10111111            ; zero -> bit 6
  STA array, x
  
  CLC
  LDA tile_selected
  SBC #$07
  TAX
  STX tile_selected

  LDA array, x
  ORA #%01000000            ; one -> bit 6
  STA array, x
ReadUpDone:

ReadDown:
  LDA $4016       ; player 1 - Down
  AND #%00000001  ; only look at bit 0
  CMP button_down
  BEQ ReadDownDone

  STA button_down
  CMP #$00
  BEQ ReadDownDone


  ; deselect tile
  LDA tile_selected
  AND #%11111000            ; invalid movement
  EOR #%00111000
  BEQ ReadDownDone

  LDX tile_selected
  LDA array, x
  AND #%10111111            ; zero -> bit 6
  STA array, x

  CLC
  LDA tile_selected
  ADC #$08
  TAX
  STX tile_selected

  LDA array, x
  ORA #%01000000            ; one -> bit 6
  STA array, x

ReadDownDone:

ReadLeft:
  LDA $4016       ; player 1 - Left
  AND #%00000001  ; only look at bit 0
  CMP button_left
  BEQ ReadLeftDone
  
  STA button_left
  CMP #$00
  BEQ ReadLeftDone

  ; deselect tile
  LDA tile_selected
  AND #%00000111            ; invalid movement
  BEQ ReadLeftDone

  LDX tile_selected
  LDA array, x
  AND #%10111111            ; zero -> bit 6
  STA array, x

  DEC tile_selected
  LDX tile_selected

  LDA array, x
  ORA #%01000000            ; one -> bit 6
  STA array, x
ReadLeftDone:

ReadRight:
  LDA $4016       ; player 1 - Right
  AND #%00000001  ; only look at bit 0
  CMP button_right
  BEQ ReadRightDone

  STA button_right
  CMP #$00
  BEQ ReadRightDone

  ; deselect tile
  LDA tile_selected
  AND #%00000111            ; invalid movement
  EOR #%00000111
  BEQ ReadRightDone

  LDX tile_selected
  LDA array, x
  AND #%10111111            ; zero -> bit 6
  STA array, x

  INC tile_selected
  LDX tile_selected

  LDA array, x
  ORA #%01000000            ; one -> bit 6
  STA array, x

ReadRightDone:
  RTS

setNeighborsVisib:
  ; Load clicked tile from the stack
  LDA tile_selected
  ; We will use an iterate algorithm to search
  ; the neighbors, avoiding recursion we save memory
  ; in case of a big board
  ; First we add the clicked tile to the iterative array (starts at $200)
  LDY #$00
  STA queue, y
  INY

CheckVisib:
  CPY #$00
  BNE continue_while
  JMP EndIterative
continue_while:


  DEY
  LDA queue, y
  STA temp

  LDX temp
  LDA array, x            ; Load the tile byte information
  
  AND #%00100000          ; check if flag
  BNE CheckVisib

  LDA array, x
  AND #$80                ; Get the visibility bit
  BNE CheckVisib          ; If tile is not visible, start iterativeLoop

  ; Set the visibility bit
  LDX temp
  LDA array, x
  ORA #$80
  STA array, x

  ; Check if selected tile is zero or a numbered tile
  ; TXA
  LDA array, x
  AND #%00001111
  ; CMP #$00
  BNE CheckVisib

TopNeighbor:
  
  ; Go to the top neighbor
  ; Test if upper bound exists
  TXA
  AND #$f8
  BEQ RigthNeighbor   ; In case the upper bound doesn't exist, branch
  ; Add TopNeighbor to iterative array
  TXA
  CLC
  SBC #$07
  
  STA queue, y
  INY

RigthNeighbor:
  
  ; Go to the right neighbor
  ; Test if righter bound exists
  TXA
  AND #$07
  CMP #$07
  
  BEQ BotNeighbor     ; In case the righter bound doesn't exist, branch
  ; Add RightNeighbor to iterative array
  TXA
  CLC
  ADC #$01
  
  STA queue, y
  INY

BotNeighbor:
  
  ; Go to the bot neighbor
  ; Test if lower bound exists
  TXA
  AND #$38
  CMP #$38
  BEQ LeftNeighbot    ; In case the lower bound doesn't exist, branch
  ; Add BotNeighbor to iterative array
  TXA
  CLC
  ADC #$08
  
  STA queue, y
  INY

LeftNeighbot:
  
  ; Go to the left neighbor
  ; Test if lefter bound exists
  TXA
  AND #%00000111
  BEQ CheckVisib    ; In case the lefter bound doesn't exist, branch to the start again

  ; TXA
  ; AND #$08
  ; CMP #$08
  ; BEQ CheckVisib    ; In case the lefter bound doesn't exist, branch to the start again
  ; Add LeftNeighbot to iterative array
  TXA
  CLC
  SBC #$00
  
  STA queue, y
  INY

TopLeft:
  TXA
  AND #%00000111      ; left margin
  BEQ TopRight

  TXA
  AND #$f8
  BEQ TopRight     ; test up
  
  TXA
  CLC
  SBC #$08
  
  STA queue, y
  INY


TopRight:

  TXA
  AND #$07
  CMP #$07      
  BEQ BotLeft   ; test right

  TXA
  AND #$f8
  BEQ BotLeft     ; test up
  
  TXA
  CLC
  SBC #$06
  
  STA queue, y
  INY

BotLeft:
  TXA
  AND #%00000111      ; left margin
  BEQ BotRight

  TXA
  AND #$38
  CMP #$38
  BEQ BotRight

  TXA
  CLC
  ADC #$07
  
  STA queue, y
  INY

BotRight:

  ; TXA
  ; AND #$07
  ; CMP #$07      
  ; BEQ end_border   ; test right  
  
  ; TXA
  ; AND #$38
  ; CMP #$38
  ; BEQ end_border

  ; TXA
  ; CLC
  ; ADC #$09
  
  ; STA queue, y
  ; INY
end_border:

  JMP CheckVisib  
EndIterative:
  RTS

gameover:
  LDX #$00
init_game_over:
  LDA array, x
  ORA #$80
  STA array, x
  INX
  CMP #$40
  BNE init_game_over

  RTS



;;;;;;;;;;;;;;  
  
  
  
  .bank 1
  .org $E000
palette:
  .db $0F,$01,$20,$10,$0F,$19,$20,$10,$0F,$06,$20,$10,$3C,$3D,$3E,$0F
  .db $0F,$01,$20,$10,$0F,$19,$20,$10,$0F,$06,$20,$10,$3C,$3D,$3E,$0F

field:
  .db $01, $02, $01, $01, $01, $0B, $0B, $02
  .db $0B, $02, $0B, $01, $01, $03, $0B, $02
  .db $01, $02, $01, $01, $00, $01, $01, $01
  .db $00, $00, $00, $00, $00, $00, $00, $00
  .db $00, $00, $00, $00, $01, $01, $01, $00 
  .db $00, $00, $00, $01, $02, $0B, $02, $01
  .db $00, $00, $00, $01, $0B, $03, $0B, $01
  .db $00, $00, $00, $01, $01, $02, $01, $01

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

