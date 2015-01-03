(* Simple bookmarking script

   Usage:
   ./bookmark [--file -f] entry page

  (entry is a book or something)

*)

(* Function definitions *)

fun load_file (file) =
    let
	val ins = TextIO.openIn file
	fun f xs =
	    case xs of
		NONE => (TextIO.closeIn ins; [])
	      | _ => (valOf xs) :: f (TextIO.inputLine ins)
    in
	f (TextIO.inputLine ins)
    end

fun init_writer file =
    let
	val outs = TextIO.openAppend file
	fun f x = TextIO.output(outs, x)
    in
	f
    end

fun parse_file_command al =
    case al of
	[] => raise List.Empty
      | x::xs => if x = "-f"
		 then SOME (hd xs)
		 else NONE

fun format_entry out =
    case out of
	[] => "\n"
      | x::[] => x ^ format_entry [] 
      | x::xs => x ^ " : " ^ format_entry xs 

(* Execution *)
val args = CommandLine.arguments()
val cmd = parse_file_command (args)

val entry = case cmd of NONE => args
		     | _ => (tl (tl args))

val file = case cmd of NONE => ".bookmarks"
		     | _ => valOf cmd

val lines = load_file(file)

val f_entry = format_entry(entry)

(*val output = format_output(lines, f_entry)*)

val writer = init_writer(file)
val _ = writer f_entry

val _ = OS.Process.exit(OS.Process.success)
