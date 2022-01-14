export function getPhoneNumberType(item){
    let type = ''
    switch(item) {
        case 'mob':
            type = "Mobile"
            break
        case 'home':
            type = "Home"
            break
        case 'work':
            type = "Work"
            break
    }
    return type
}

export function getEmailType(item){
    let type = ''
    switch(item) {
        case 'work':
            type = "Work"
            break
        case 'pers':
            type = "Personal"
            break
    }
    return type
}
