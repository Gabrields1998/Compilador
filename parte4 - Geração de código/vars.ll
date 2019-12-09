; ModuleID = "meu_modulo.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

define i32 @"main"() 
{
entry:
  %"retorno" = alloca i32
  %"x" = alloca i32, align 4
  %"y" = alloca float, align 4
  store i32 0, i32* %"x"
  store float              0x0, float* %"y"
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"x"
  %".6" = call float @"leiaFlutuante"()
  store float %".6", float* %"y"
  %"x.1" = load i32, i32* %"x"
  call void @"escrevaInteiro"(i32 %"x.1")
  %"y.1" = load float, float* %"y"
  call void @"escrevaFlutuante"(float %"y.1")
  store i32 0, i32* %"retorno"
  br label %"exit"
exit:
  %"finsterson" = alloca float
  store float              0x0, float* %"finsterson"
  %"retorno.1" = load i32, i32* %"retorno"
  ret i32 %"retorno.1"
}
