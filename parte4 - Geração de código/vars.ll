; ModuleID = "meu_modulo.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

@"n" = common global i32 0, align 4
define i32 @"fatorial"(i32 %".1") 
{
entry:
  %"retorno" = alloca i32
  %"n" = alloca i32, align 4
  store i32 %".1", i32* %"n"
  %"fat" = alloca i32, align 4
  %"n.1" = load i32, i32* @"n"
  %"if_test" = icmp sgt i32 %"n.1", 0
  br i1 %"if_test", label %"iftrue", label %"iffalse"
iftrue:
  store i32 1, i32* %"fat"
  %"fat.1" = load i32, i32* %"fat"
  %"n.2" = load i32, i32* @"n"
  %"multiplicacao" = mul i32 %"fat.1", %"n.2"
  store i32 %"multiplicacao", i32* %"fat"
  %"n.3" = load i32, i32* @"n"
  %"subtracao" = sub i32 %"n.3", 1
  store i32 %"subtracao", i32* @"n"
  %"fat.2" = load i32, i32* %"fat"
  store i32 %"fat.2", i32* %"retorno"
  br label %"ifend"
iffalse:
  store i32 0, i32* %"retorno"
  br label %"ifend"
ifend:
  %"finsterson" = alloca i32
  br label %"exit"
exit:
  %"finsterson.1" = alloca float
  store float              0x0, float* %"finsterson.1"
  %"retorno.1" = load i32, i32* %"retorno"
  ret i32 %"retorno.1"
}

define i32 @"main"() 
{
entry:
  %"retorno" = alloca i32
  %".2" = call i32 @"leiaInteiro"()
  store i32 %".2", i32* @"n"
  %"fato" = alloca i32, align 4
  %"n" = load i32, i32* @"n"
  %".4" = call i32 @"fatorial"(i32 %"n")
  store i32 %".4", i32* %"fato"
  %"fato.1" = load i32, i32* %"fato"
  call void @"escrevaInteiro"(i32 %"fato.1")
  store i32 0, i32* %"retorno"
  br label %"exit"
exit:
  %"finsterson" = alloca float
  store float              0x0, float* %"finsterson"
  %"retorno.1" = load i32, i32* %"retorno"
  ret i32 %"retorno.1"
}
