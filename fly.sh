#!/bin/bash

# Simple script to fly the tello drone. First connect to drone WiFi
# Sends commands via netcat (nc)
# Only tested on mac
# Just type a letter and then [ENTER]

function send() {
    echo -n "$1" | nc -w 0 -u 192.168.10.1 8889
}

CM=20
DEG=45

while read command; do
    case $command in
        "t")
            send command
            send takeoff
        ;;
        "l")
            send land
        ;;
        "v")
            send command
            send streamon
        ;;
        "z")
            send streamoff
        ;;
        "f")
            send "flip l"
        ;;
        "w")
            send "up $CM"
        ;;
        "s")
            send "down $CM"
        ;;
        "a")
            send "left $CM"
        ;;
        "d")
            send "right $CM"
        ;;
        "u")
            send "forward $CM"
        ;;
        "j")
            send "back $CM"
        ;;
        "h")
            send "ccw $DEG"
        ;;
        "k")
            send "cw $DEG"
        ;;
    esac
done