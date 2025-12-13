output "text" {
  value = local.puzzle_input
}

output "lines" {
  value = split("\n", local.puzzle_input)
}
