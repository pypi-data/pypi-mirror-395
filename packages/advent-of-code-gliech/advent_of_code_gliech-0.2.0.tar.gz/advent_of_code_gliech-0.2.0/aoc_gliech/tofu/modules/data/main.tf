locals {
  # Source the AoC session token liko aocd does
  aoc_config_dir = pathexpand(coalesce(
    data.external.env.result.AOCD_CONFIG_DIR,
    data.external.env.result.AOCD_DIR,
    "~/.config/aocd"
  ))
  aoc_users = (
    fileexists("${local.aoc_config_dir}/tokens.json") ?
    jsondecode(file("${local.aoc_config_dir}/tokens.json")) :
    {"default" : coalesce(
      data.external.env.result.AOC_SESSION,
      (
        fileexists("${local.aoc_config_dir}/token") ?
        trimspace(file("${local.aoc_config_dir}/token")) : null
      )
    )}
  )

  # If puzzle year and day is not given through vars, try to gather the info
  # from the location of the root module, if that also fails fall back to the
  # timestamp of when the first execution of the module.
  year = coalesce(
    var.year,
    tonumber(one(regexall("20\\d\\d", abspath(path.root)))),
    time_static.now.year - (time_static.now.month<12 ? 1 : 0)
  )
  day = coalesce(
    var.day,
    tonumber(one(regexall(
      "([12]?\\d)(?:\\D*$)",
      replace(abspath(path.root), local.year, "xxxx")
    )[*][0])),
    time_static.now.month==12 ? time_static.now.day : null
  )

  # Get puzzle input from the outside (this is mainly for use with the aocd
  # runner), or from the cache file if the input was already cached, or from the
  # module if the cache is created in the same run.
  cache_file_location = format("%s/.aoc_input_%d_%02d.txt", path.root, local.year, local.day)
  puzzle_input = coalesce(var.input, (
    fileexists(local.cache_file_location) ?
    file(local.cache_file_location) :
    resource.local_file.cached_input.content
  ))
}

data "external" "env" {
  program = ["${path.module}/env.py"]
  query = {
    vars = join(",", ["AOC_SESSION", "AOCD_CONFIG_DIR", "AOCD_DIR"])
  }
}

resource "time_static" "now" {
}

data "http" "puzzle_input" {
  count = fileexists(local.cache_file_location) ? 0 : 1

  url = "https://adventofcode.com/${local.year}/day/${local.day}/input"
  request_headers = {
    Cookie = "session=${local.aoc_users[var.aoc_user]}"
  }

  lifecycle {
    postcondition {
      condition     = self.status_code==200
      error_message = "Status code invalid"
    }
  }
}

resource "local_file" "cached_input" {
  filename        = local.cache_file_location
  file_permission = "0644"
  content = chomp(coalesce(one(
    data.http.puzzle_input[*].response_body),
    "should never be used"
  ))

  lifecycle {
    ignore_changes = [content]
  }
}
