; ModuleID = "meu_modulo.bc"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"n" = common global i32 undef, align 4
@"m" = common global float undef, align 4
define i32 @"fatorial"(i32 %".1") 
{
entry:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  %"n" = alloca i32, align 4
  %"fat" = alloca i32, align 4
  %"n.1" = load i32, i32* @"n"
  %"if_test" = icmp sgt i32 %"n.1", 0
  %"fat.1" = load i32, i32* %"fat"
  store i32 %"fat.1", i32* @"n"
  %"fat.2" = load i32, i32* %"fat"
  %"n.2" = load i32, i32* @"n"
  %"multiplicacao" = mul i32 %"fat.2", %"n.2"
  store i32 %"multiplicacao", i32* %"fat"
  %"n.3" = load i32, i32* @"n"
  %"subtracao" = sub i32 %"n.3", 1
  store i32 %"subtracao", i32* @"n"
exit:
}

define i32 @"main"() 
{
entry:
  %"retorno" = alloca i32
  store i32 0, i32* %"retorno"
  store float 0x4024333340000000, float* @"m"
exit:
}
