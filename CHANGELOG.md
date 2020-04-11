# Changelog

## 4.3.2

Intermediate releases: 4.3.1

* add `cms dryrun` command it stest the variable dryrun
* add `cms set` command that does a list of the variables
* add `cms var` command that does a list of the variables
* add `cms debug=on` command works the same way as `cms debug on`
* add `cms dryrun=on` command works the same way as `cms dryrun on`
* changed all use of `Variables(filename=..)` to ` Variables()`

## 4.3.0

* Introduced a selective load based on the command name, which reduces
  execution time significantly. We see improvement sof 1 second which is
  significant when doing interactive work outside of the shell with just
  the commandline.
* Removal of the old plugin command

## 4.2.22

* move some of the tests that belong into cmd5 from other repos


