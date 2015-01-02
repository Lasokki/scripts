(* Simple bookmarking script

   Usage:
   ./bookmark [--file -f] entry page

  (entry is a book or something)

*)

(* Some required values *)
val default_file = ".bookmarks"

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

fun parse_entry_to_write (f, al) =
    case f of
	NONE => al
      | _ => (tl (tl al))

fun format_entry out =
    case out of
	[] => "\n"
      | x::[] => x ^ format_output [] 
      | x::xs => x ^ " : " ^ format_output xs 

fun choose_writer c =
    case c of
	NONE => init_writer (default_file)
      | _ => init_writer (valOf c)


(* Execution *)
val args = CommandLine.arguments()
val cmd = parse_file_command (args)
val entry = parse_entry_to_write (cmd, args)
val f_entry = format_entry(entry)
val writer = choose_writer(cmd)
val _ = writer f_output
val _ = OS.Process.exit(OS.Process.success)
