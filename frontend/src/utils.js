export default function getType(item){
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
        case 'pers':
            type = "Personal"
            break
    }
    return type
}
