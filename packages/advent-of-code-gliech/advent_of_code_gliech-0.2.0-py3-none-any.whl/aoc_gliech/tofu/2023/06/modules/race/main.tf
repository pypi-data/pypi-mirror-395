variable "time" {
  type = number
}

variable "distance" {
  type = number
}

locals {
  x = pow(pow(var.time, 2) - 4 * var.distance, 0.5)
  min_win = floor((var.time - local.x) / 2 + 1)
  max_win = ceil((var.time + local.x) / 2 - 1)
}

output "result" {
  value = local.max_win - local.min_win + 1
}
