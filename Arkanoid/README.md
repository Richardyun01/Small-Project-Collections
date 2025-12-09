# Arkanoid
3D Arkanoid game written in C++ based on OpenGL
- OS: Windows 11 ver.22H2(OS build 22621.2283)
- Compiler: Code::Blocks 20.03 GCC MinGW-W64 project (version 8.1.0, 32/64 bit, SEH)
- How to Compile: https://wiki.codeblocks.org/index.php/Using_FreeGlut_with_Code::Blocks
  - 1. Download freeglut 3.0.0 MinGW Package from https://www.transmissionzero.co.uk/software/freeglut-devel/
  - 2. Copy freeglut.dll to C:\Program Files (x86)\CodeBlocks\minGW
  - 3. Change wizard.script in 
    - 3-1. project.AddLinkLib(_T("Glut32")); -> project.AddLinkLib(_T("freeglut"));
    - 3-2. if (!VerifyLibFile(dir_nomacro_lib, _T("glut32"), _T("GLUT's"))) return false; -> if (!VerifyLibFile(dir_nomacro_lib, _T("freeglut"), _T("GLUT's"))) return false;"
  - 4. Change glut.cbp in
    - 4-1. <Add library="Glut32" /> -> <Add library="freeglut" />
- How to run: Execute 'Build and run'
