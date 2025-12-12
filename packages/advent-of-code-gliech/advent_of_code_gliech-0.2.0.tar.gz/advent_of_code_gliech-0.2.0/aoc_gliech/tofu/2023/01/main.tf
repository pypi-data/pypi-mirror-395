variable "puzzle_input" {
  type    = string
  default = null
}

module "data" {
  source = "../../modules/data"
  input  = var.puzzle_input
}

locals {
  digits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
  number_lookup = merge(
    {for i in range(length(local.digits)) : local.digits[i] => i+1},
    {for i in range(10) : i => i}
  )
}

output "solution_a" {
  value = sum([
    for char_array in [
      for line in module.data.lines : [
        for char in split("", line) : char if can(tonumber(char))
      ]
    ] : tonumber(join("", [char_array[0], reverse(char_array)[0]]))
  ])
}

output "solution_b" {
  value = sum([
    for line in module.data.lines :
    tonumber(join("", [
      local.number_lookup[one(regex("^.*?([[:digit:]]|${join("|", local.digits)}).*$", line))],
      local.number_lookup[one(regex("^.*([[:digit:]]|${join("|", local.digits)}).*?$", line))]
    ]))
  ])
}
