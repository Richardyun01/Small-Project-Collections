# Recursive-Parser
Recursive Parsing program written in C++

Created by [Richardyun01](https://github.com/Richardyun01) and [novaprospectCAU](https://github.com/novaprospectCAU). Original repesitory is [here](https://github.com/novaprospectCAU/RDP).

주 실행 방법(제일 먼저 이 방법을 사용해서 실행해주시길 바랍니다.)
- OS: Windows 11 ver.22H2(OS build 22621.2283)
- HW: Intel Core i5-8265U 이상
- Compiler: Code::Blocks 20.03 GCC MinGW-W64 project (version 8.1.0, 32/64 bit, SEH)
- 컴파일 방법: 
- a. codeblocks – binary releases - codeblocks-20.03mingw-setup 설치
- b. C:\CodeBlocks\MinGW\bin 을 환경변수 Path 에 추가
- c. RecursiveParser.cbp 가 존재하는 위치에서 g++ main.cpp
- 실행 방법: RecursiveParser/bin/Debug -> cmd 실행 'RecursiveParser.exe input1.txt' 입력
- 컴파일 시 주의 사항 : 최소 C++11 버전이 요구됩니다. 이하 버전에서는 돌아가지
않습니다.
- 실행 시 주의 사항 : RecursiveParser.exe 와 input 파일이 모두 존재하는 위치에서 실행해야
합니다.

보조 실행 방법(위의 방법이 작동하지 않는 경우 실행해주시길 바랍니다.)
- OS: macOS Sonoma (Ver. 14.0)
- HW: Intel Core i7(MacBook Pro) 이상
- Compiler: Apple Clang ver.14.0.3
- 컴파일 방법 : 터미널 – g++ -std=c++11 ./RecursiveParser/main.cpp
- 실행 방법: ./a.out ./RecursiveParser/bin/Debug/input1.txt
다른 파일을 시도하려면 input1.txt 대신 다른 텍스트 파일을 넣으면 됩니다.
-컴파일 시 주의 사항 : 최소 C++11 버전이 요구되므로, 컴파일 시 -std=c++11 가 없을 경우
Warning 혹은 Error 가 발생할 수 있습니다.
