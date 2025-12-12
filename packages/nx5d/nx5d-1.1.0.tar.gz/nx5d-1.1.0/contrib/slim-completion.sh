
_slim_completion() {
    local current=${COMP_WORDS[$COMP_CWORD]}

    if [ $COMP_CWORD == 1 ]; then
        local suggest=($(slim proposals? $current))
    elif [ $COMP_CWORD == 2 ]; then
        local suggest=($(slim commands? $current))
    else
        return
    fi

    COMPREPLY=(${suggest[@]})
}

_kmc3_from_pilatus_completion() {
    local current=${COMP_WORDS[$COMP_CWORD]}

    if [ $COMP_CWORD == 1 ]; then
        local suggest=($(kmc3-from-pilatus "$current"?))
    else
        return
    fi

    COMPREPLY=(${suggest[@]})
}

complete -F _slim_completion slim
complete -F _kmc3_from_pilatus_completion kmc3-from-pilatus
