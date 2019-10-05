; Author: tokumaru
; http://forums.nesdev.com/viewtopic.php?%20p=58138#58138
;----------------------------------------------------------------
; constants
;----------------------------------------------------------------
PRG_COUNT = 1 ;1 = 16KB, 2 = 32KB
MIRRORING = %0001 ;%0000 = horizontal, %0001 = vertical, %1000 = four-screen

;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000

   ;NOTE: declare variables using the DSB and DSW directives, like this:

   ;MyVariable0 .dsb 1
   ;MyVariable1 .dsb 3

   .ende

   ;NOTE: you can also split the variable declarations into individual pages, like this:

   ;.enum $0100
   ;.ende

   ;.enum $0200
   ;.ende

;----------------------------------------------------------------
; iNES header
;----------------------------------------------------------------

   .db "NES", $1a ;identification of the iNES header
   .db PRG_COUNT ;number of 16KB PRG-ROM pages
   .db $01 ;number of 8KB CHR-ROM pages
   .db $00|MIRRORING ;mapper 0 and mirroring
   .dsb 9, $00 ;clear the remaining bytes

;----------------------------------------------------------------
; program bank(s)
;----------------------------------------------------------------

   .base $10000-(PRG_COUNT*$4000)

Reset:
    LDA #$ff
    STA $0101
    STA $01

    LDA #$44
    STA $0102
    STA $02

    LDA #$7c
    STA $0103

    LDA #$03
    STA $06
    LDA #$01
    STA $07

    LDA #$04
    STA $05

    LDA #$06
    STA $04

    LDX #$01
    LDY #$02

    LDA #$57
    ; Test all four DEC
    EOR #$01
    EOR $01
    EOR $01, X
    EOR $0101
    EOR $0101, X
    EOR $0101, Y
    EOR ($03, X)
    EOR ($05), Y
    BRK
NMI:
   ;NOTE: NMI code goes here
IRQ:

   ;NOTE: IRQ code goes here

;----------------------------------------------------------------
; interrupt vectors
;----------------------------------------------------------------

   .org $fffa

   .dw NMI
   .dw Reset
   .dw IRQ
