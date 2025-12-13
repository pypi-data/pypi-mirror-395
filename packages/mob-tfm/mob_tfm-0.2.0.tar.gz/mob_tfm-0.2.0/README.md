# `tfm`

A set of tools to quick up MySql/MariaDB table prototyping


## **Installation**:
```bash
$ pip install mob-tfm
```

### **Usage**:

```console
$ tfm [OPTIONS] COMMAND [ARGS]...
```

### **Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

# **Commands**:

* `version`: Show the current version of Mob TFM.
* `unspine`: &#x27;Unspine&#x27;/print the doc of a list of tfm...
* `doctor`: Show information about Mob TFM.
* `parse`: fill a mariaDB/MySQL database table with...
* `generate`: fill a mariaDB/MySQL database table with...
* `config`: Create or Edit the configuration for...
* `explain`: Open and page the documentation for one or...

## `tfm version`

Show the current version of Mob TFM.

### **Usage**:

```bash
$ tfm version [OPTIONS]
```

### **Options**:

* `--help`: Show this message and exit.

## `tfm unspine`

&#x27;Unspine&#x27;/print the doc of a list of tfm generators inside of a pager (alternative screen)

### **Usage**:

```bash
$ tfm unspine [OPTIONS] GENERATORS
```

### **Arguments**:

* `GENERATORS`: [required]

### **Options**:

* `-p / --pretty`: force activation markdown styling/ may cause issue on old terminals
* `--help`: Show this message and exit.

## `tfm doctor`

Show information about Mob TFM.
Can be considered as a &#x27;about&#x27; command.

### **Usage**:

```bash
$ tfm doctor [OPTIONS]
```

### **Options**:

* `--help`: Show this message and exit.

## `tfm parse`

fill a mariaDB/MySQL database table with data contained in a csv file.

### **Usage**:

```bash
$ tfm parse [OPTIONS] FILE
```

### **Arguments**:

* `FILE`: [required]

### **Options**:

* `-u, --user TEXT`: Database user name 
* `-P, --password TEXT`: Database user password 
* `-d, --database TEXT`: Database name 
* `-t, --table TEXT`: The Database Table to target 
* `-h, --host TEXT`: The Databse host  [default: localhost]
* `-p, --port INTEGER`: The database port  [default: 3306]
* `-r, --rows INTEGER`: Number of rows to read (negative for all lines)  [default: 20]
* `--preview-only / --no-preview-only`: If --preview tfm won&#x27;t try to fill the table, only preview them.  [default: no-preview-only]
* `--help`: Show this message and exit.

## `tfm generate`

fill a mariaDB/MySQL database table with fake data based on a format string.

### **Usage**:

```console
$ tfm generate [OPTIONS] FORMAT
```

### **Arguments**:

* `FORMAT`: [required]

### **Options**:

* `-s, --seed INTEGER`: Seed for the random generator.
* `-u, --user TEXT`: Database user name.
* `-P, --password TEXT`: Database user password.
* `-d, --database TEXT`: Database name.
* `-t, --table TEXT`: Database table name.
* `-h, --host TEXT`: Database host.  [default: localhost]
* `-p, --port INTEGER`: Database port.  [default: 3306]
* `--optimized / --no-optimized`: Use optimized generation methods.  [default: no-optimized]
* `-r, --rows INTEGER`: Number of rows to generate.  [default: 20]
* `--help`: Show this message and exit.

## `tfm config`


Create or Edit the configuration for better use of tfm.

### **Usage**:

```bash
$ tfm config [OPTIONS]
```

### **Options**:

* `-v, --view`: View current configuration
* `--help`: Show this message and exit.

## `tfm explain`

Open and page the documentation for one or more commands from `docs/commands/README.<command>.md`.

### **Usage**:

```console
$ tfm explain [OPTIONS] COMMANDS
```
 

### **Arguments**:

* `COMMANDS`: [required]

### **Options**:

* `-p / --pretty`: force activation markdown styling/ may cause issue on old terminals.
* `--help`: Show this message and exit.
