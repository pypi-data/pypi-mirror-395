variable "puzzle_input" {
  type    = string
  default = null
}

module "data" {
  source = "../../modules/data"
  input  = var.puzzle_input
}

locals {
  input_by_line = [for line in module.data.lines : regexall("\\d+", line)]
  input_by_race = {
    for race in range(length(local.input_by_line[0])) :
    race => [for line in local.input_by_line : line[race]]
  }
}

module "part_a" {
  for_each = local.input_by_race

  source = "./modules/race"
  time     = each.value[0]
  distance = each.value[1]
}

locals {
   results = values(module.part_a)[*].result
}

output "solution_a" {
  # I do not know how to reduce with multiplication in tofu.
  value = local.results[0]*local.results[1]*local.results[2]*local.results[3]
}

locals {
  part_b_input = [for line in module.data.lines : join("", regexall("\\d+", line))]
}

module "part_b" {
  source = "./modules/race"
  time     = local.part_b_input[0]
  distance = local.part_b_input[1]
}

output "solution_b" {
  value = module.part_b.result
}
