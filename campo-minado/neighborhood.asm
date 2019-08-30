
setNeighborsVisib:
    ; Load clicked tile from the stack
    PLA
    ; We will use an iterate algorithm to search
    ; the neighbors, avoiding recursion we save memory
    ; in case of a big board
    ; First we add the clicked tile to the iterative array (starts at $200)
    LDY #$00
    STA $0200, y
    INY

    CheckVisib:
        TAX
        LDA $0100, x            ; Load the tile byte information
        AND #$80                ; Get the visibility bit
        CMP #$80
        BNE IterativeLoop       ; If tile is not visible, start iterativeLoop

        TYA
        CMP #$01                ; If Y == 1 we reached the end of the iterativeLoop
        BEQ EndIterative
    
    IterativeLoop:
        ; Set the visibility bit
        ORA #$80
        STA $0100, x
        DEY                     ; Decrement iterative array

        TopNeighbor:
            TXA
            ; Go to the top neighbor
            ; Test if upper bound exists
            AND #$f8
            CMP #$00
            BEQ RigthNeighbor   ; In case the upper bound doesn't exist, branch
            ; Add TopNeighbor to iterative array
            TXA
            CLC
            SBC #$08
            STA $0200, y
            INY

        RigthNeighbor:
            TXA
            ; Go to the right neighbor
            ; Test if righter bound exists
            AND #$07
            CMP #$07
            BEQ BotNeighbor     ; In case the righter bound doesn't exist, branch
            ; Add RightNeighbor to iterative array
            TXA
            CLC
            ADC #$01
            STA $0200, y
            INY

        BotNeighbor:
            TXA
            ; Go to the bot neighbor
            ; Test if lower bound exists
            AND #$38
            CMP #$37
            BEQ LeftNeighbot    ; In case the lower bound doesn't exist, branch
            ; Add BotNeighbor to iterative array
            TXA
            CLC
            ADC #$08
            STA $0200, y
            INY

        LeftNeighbot:
            TXA
            ; Go to the left neighbor
            ; Test if lefter bound exists
            AND #$0f
            CMP #$00
            BEQ CheckVisib    ; In case the lefter bound doesn't exist, branch to the start again

            AND #$08
            CMP #$08
            BEQ CheckVisib    ; In case the lefter bound doesn't exist, branch to the start again
            ; Add LeftNeighbot to iterative array
            TXA
            CLC
            SBC #$01
            STA $0200, y
            INY
        
        LDA #$00
        CMP #$00                ; Go back to the start
        BEQ CheckVisib


    EndIterative:
        BRK