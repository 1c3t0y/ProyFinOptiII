from Redes import FloydWarshal, Dijkstra
from Entera import branch_and_bound, enumeracion_implicita


switcher_metodos_redes = {
    '1': Dijkstra.MetodoDijkstra,
    '2': FloydWarshal.MetodoFloyd
}

switcher_metodos_entera = {
    '1': branch_and_bound.BranchAndBound,
    '2': enumeracion_implicita.EnumeracionImplicita
}
