from Redes import FloydWarshal
from Entera import branch_and_bound


switcher_metodos_redes = {
    '1': FloydWarshal.MetodoFloyd
}

switcher_metodos_entera = {
    '1': branch_and_bound.BranchAndBound
}
