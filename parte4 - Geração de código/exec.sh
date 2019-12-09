echo "executando comandos..."

llc -filetype=obj vars.ll -o vars.o
clang -shared -fPIC io.c -o io.so
clang -S -emit-llvm -o io.bc -c io.c
llc -filetype=obj io.bc -o io.o
clang vars.o io.o -o vars.exe