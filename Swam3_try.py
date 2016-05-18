import adapter_swam3
Swam3 = adapter_swam3.Adapter(40100,'COM10','log')
Swam3.SendTenCmd("ss_reset")

