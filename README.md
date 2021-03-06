# Topy / TodoFlow #

# Overview #

Topy module provides API for interacting with todo lists in plain text files with [taskpaperlike][] format with powerful query syntax. It provides functions to modify lists and to convert them to markdown, html and XML used in [Alfred2][] workflow. See utilities for examples of what can be done with it.

You can jump straight to Alfred2 workflows if you here for that.

# Usage #

##### topy #####

Use *from_file* and *from_files** functions to create object that represents todo list. Module also provides functions for basic modifications of list using items id (*do*, *tag*, *remove*, *get_content*, *add_new_subtask*).

\* when creating one list from multiple files each list is packed into project with title identical to name of source file.

##### topy.lists #####

Provides functions to add, remove and retrieve globally available list of path to active todo lists. Those paths are stored in tab-separated text file, its location can be specified in config.py.  

##### topy.todolist #####

Defines classes TodoList, Note, Project, Task and operations on them.

For more read comments in source files.

## List Syntax ##

- Task is line that begins with '- ', can be indented with tabs.
- Project is every line that is not task and ends with ':' with eventual trailings tags after that colon.
- Every other line is a note.
- Tag is word preceded by '@' with eventual parameter in parenthesis (e.g. **@today**, **@done(2013-03-01)**).
- Structure of list is defined by indentation levels of items.

## Query Syntax ##

You can filter items in the list by searching for the words, tags (e.g. **@today**) or using argument-operator-value syntax.

##### Arguments:

- project - title of any parent project in hierarchy
- uniqueid
- content - line without formatting and trailing tags
- type - task / note / "project"
- level - indentation level
- parent - any parent in hierarchy
- index - index in list, relative to closest parent, starts with 0. For example:

		Parent project:
			- task1
			subproject:
				- task2
				- task3
			- task4

Both task1 and task2 have index 0, subproject and task3 have index 1, task4 has index 2.

- tag - parameter of tag

##### Operators: #####

- =
- !=
- \< - values are compared lexicographically (it just string comparision)
- \>
- \<=
- \>=
- matches - match with regexp
- contains, $ (those are synonyms)

Two queries joined by *and* are query, two queries joined by *or* are query, query can be negated with *not* operator. Words that are part of syntax can be escaped by putting them in double quotes "".

Full grammar is in filterpredicate.py source file.

# Instalation & Configuration #

For now I'm not providing *setup.py*, so to use it from anywhere you need to add directory that contains topy folder to python path. Main configuration file is in *topy/config.py*, options are described there. Several utilities require additional configuration.

# Utilities #

Some examples what can be done with this module and other tools for working with plain text todo lists. Those are scripts I use on daily basis with my todo list (Projects.todo, Onhold.todo and Inbox.todo).

## tp ##

	Command line interface.
	
	usage: tp [-h] [-q QUERY] [-p [PATHS [PATHS ...]]] [--not-colored]
			  [--markdown] [--with-ids] [--html] [--css CSS] [--countdow	]	
			 [--dont-indent	
	
	Filter todo list.
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -q QUERY, --query QUERY
							predicate to filter with
	  -p [PATHS [PATHS ...]], --paths [PATHS [PATHS ...]]
							paths to files containg todo list, defaults 	to paths	
								stored in topy.lists (see config.py)	
	  --not-	colored, -nc    not colored output	
	  --mark	down, -md       print as markdow	
	  --with	-ids, -ids      print with items	ids	
	  --html	                print as htm	
	  --css CSS             css stylesheet, only valid with --html	
	  --countdown, -cd      print as countdown
	  --dont-indent         don't indent lines

![tp_screen_shot][]

## SublimeTodoFlow ##

SublimeText 2 package, read more in [its readme][SublimeReadme].

## TodoFlow2 Alfred 2 Workflow ##

*Requires additional configuration of paths in config.py inside workflow folder*

##### *q* keyword

Displays all tasks in [active lists][], you can filter them by typing query.

- ↩ - tags task as **@done**
- ⌘+↩ - **new, kinda experimental feature** performs action depending on tags of task, at the moment to change behaviour you need to modify tag_dependand_action function in main.py
	- if task has tag **@file** or **@web** tries to open parameter of that tag
	- if taks has tag **@search** or **@research** opens Alfred2 with query *g {content of task}*
	- if task has tag **@download** or **@tvseries** opens Alfred2 with query  *pb {content of task}*
	- always puts content of task to clipboard
- fn+↩ - removes task from list

![alfred-q][]

In config.py you can set dictionary of one-letter abbreviations for queries. To use them type **q** and then previously defined  abbreviation (without space). Abbreviations can be chained with *and*.

Examples:

	quick_query_abbreviations = {
    		'n': '@next',
    		'd': 'not @done',
    	}

- **qn** - search for tasks tagged with **@next**
- **qd** - search for tasks *not* tagged with **@done**
- **qnd** - search for tasks tagged with **@next** *and not* tagged with **@done** 
	

##### *a* keyword #####


Displays list of all projects in [active lists][].
Type task and hit ↩ to append task to selected project, you can filter projects by typing query after ';'.

![alfred-a][]

##### *remove list* keywords #####

- ↩ - remove list from active lists

##### *add list* file action #####

Adds list to active lists

##### icons #####

- ![task][] - task
- ![done][] - item tagged as **@done**
- ![project][] - project
- ![note][] - note

## Inbox Alfred 2 Workflow ##

*Requires additional configuration of paths in inbox.py inside workflow folder*

##### *in* keyword & fallback search ######

Appends typed task with date stamp to Inbox.todo. 

![alfred-in][]

##### first hotkey #####

Appends selected text to Inbox.todo with date stamp. 

##### second hotkey #####

Appends selected mails in Mail.app to Inbox.todo, see [mail-to-inbox][]


---

*You can configure following scripts in **utilities/config.py**. That includes path to todo lists, what is very important.*

---

### open_html

	usage: open_html.py [-h] [-q QUERY] [-p [PATHS [PATHS ...]]] [--css CSS]
	
	Open page with todo list in default browser.
	
	optional arguments:
		-h, --help            show this help message and exit
		-q QUERY, --query QUERY
						predicate to filter with
		-p [PATHS [PATHS ...]], --paths [PATHS [PATHS ...]]
						paths to files containg todo list, defaults to paths
						stored in topy.lists (see config.py)
		--css CSS             css stylesheet, only valid with --html

3 css styles are included.

### archive ###

Moves **@done** tasks from active todo lists to Archive.todo.

### inbox ###

Appends tasks to Inbox.todo with date stamp as parameter of **@in** tag.

### mail-to-inbox ###

AppleScript that's puts selected tasks in Mail.app to Inbox.todo in following format:

\- subject **@in(**date received**)** **@person(**sender**)** **@mail(**message://...**)**

Requires additional configuration in script itself. I know nothing about AppleScript so it may be not very pretty.

### log_to_day_one ###

Creates entry in [Day One][] with tasks that were done today.

### tvcal ###

Adds titles of tv series that will air in upcoming 24 hours to Inbox.todo, requires account at <http://www.pogdesign.co.uk/cat/>

### update_lists ###

Provides functions to update recurring tasks.

* Tasks in Onhold.todo with tag **@waiting(some-date-in-ISO-8601-format)** are added to Inbox.todo at that date.
* Tasks in Onhold.todo tagged with **@weekly(some-day-of-the-week)** are added to Inbox.todo at that day. 
* Tag **@done** is removed from tasks in Daily project in main todo list.

At the moment no tasks are removed from Onhold.todo.

### end_the_day

Joins several of other scripts. Launchd runs it for me at the and of the day. 

### reminders_to_topy ###

Imports items from *Inbox* list in Reminders.app to Inbox file,
some path must be adjusted in AppleScript *reminders_to_topy.applescript*.

It allows to put items into Inbox with Siri on iOS (just put reminder in *Inbox* list and import it when on Mac or set this script in launchd).

## NerdTool / GeekTools ##

Scripts I use to put todo lists on Desktop with Nerdtools.

### NerdTool Exported Logs ###

It looks like this:

![nerd_tools][]

### print_next ###

Prints actionable tasks.

### print_today ###

Prints tasks planned for today.

### print_deadlines

Prints tasks that have due date with count of days that left to that date.

### count_inbox ###

Prints out number of items in Inbox.todo.


© 2013 Piotr Wilczyński
[@bevesce][]

[taskpaperlike]: http://www.hogbaysoftware.com/products/taskpaper
[SublimeReadme]: https://github.com/bevesce/TodoFlow/tree/master/utilities/SublimeTodoFlow
[Day One]: http://dayoneapp.com
[tp_screen_shot]: http://bvsc.nazwa.pl/img/TodoFlow/tp.png "tp iTerm screenshot"
[nerd_tools]: http://bvsc.nazwa.pl/img/TodoFlow/nerdtool.png "NerdTool screenshot"
[Alfred2]: http://v2.alfredapp.com
[alfred-a]: http://bvsc.nazwa.pl/img/TodoFlow/TodoFlow2-a.png
[alfred-q]: http://bvsc.nazwa.pl/img/TodoFlow/TodoFlow2-q.png
[alfred-in]: http://bvsc.nazwa.pl/img/TodoFlow/TodoFlow2-in.png
[@bevesce]: https://twitter.com/@bevesce
[done]: http://bvsc.nazwa.pl/img/TodoFlow/done.png
[task]: http://bvsc.nazwa.pl/img/TodoFlow/task.png
[project]: http://bvsc.nazwa.pl/img/TodoFlow/project.png
[note]: http://bvsc.nazwa.pl/img/TodoFlow/note.png

