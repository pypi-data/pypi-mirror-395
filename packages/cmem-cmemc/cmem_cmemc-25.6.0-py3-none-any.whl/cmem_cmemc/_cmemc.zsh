#compdef cmemc

_cmemc_completion() {
    local -a completions
    local -a completions_with_descriptions
    local -a response
    (( ! $+commands[cmemc] )) && return 1

    response=("${(@f)$(env COMP_WORDS="${words[*]}" COMP_CWORD=$((CURRENT-1)) _CMEMC_COMPLETE=zsh_complete cmemc)}")

    for type key descr in ${response}; do
        if [[ "$type" == "plain" ]]; then
            if [[ "$descr" == "_" ]]; then
                completions+=("$key")
            else
                completions_with_descriptions+=("$key":"$descr")
            fi
        elif [[ "$type" == "dir" ]]; then
            _path_files -/
        elif [[ "$type" == "file" ]]; then
            _path_files -f
        fi
    done

    if [ -n "$completions_with_descriptions" ]; then
        _describe -V unsorted completions_with_descriptions -U
    fi

    if [ -n "$completions" ]; then
        compadd -U -V unsorted -a completions
    fi
    # Other than the standard click completion function, we re-added this line
    # in order to have working completions for task IDs
    compstate[insert]="automenu"
}

if [[ $zsh_eval_context[-1] == loadautofunc ]]; then
    # autoload from fpath, call function directly
    _cmemc_completion "$@"
else
    # eval/source/. command, register function for later
    compdef _cmemc_completion cmemc
fi

