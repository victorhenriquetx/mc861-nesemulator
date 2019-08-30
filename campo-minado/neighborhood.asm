
setNeighborsVisib:
    ; Load clicked tile from the stack
    PLA
    ; We will use an iterate algorithm to search
    ; the neighbors, avoiding recursion we save memory
    ; in case of a big board
    
    TAX
    TopNeighbor:
        ; Go to the top neighbor
        ; Test if upper bond exists
        SBC #$08
        BMI RigthNeighbor   ; In case the upper bound doesn't exist

    RigthNeighbor:
        ; Go to the right neighbor
        ; Test if righter bond exists
        AND #$07
        CMP #$06
        BEQ BotNeighbor

    BotNeighbor:
        ; Go to the bot neighbor
        ; Test if lower bond exists
        AND #$38
        CMP #$37
        BEQ LeftNeighbot

    LeftNeighbot:
        ; Go to the left neighbor
        ; Test if lefter bond exists
        AND #l$0f
        CMP #$00
        BEQ EndIterative

        AND #$08
        SBC #$08
        BEQ EndIterative
