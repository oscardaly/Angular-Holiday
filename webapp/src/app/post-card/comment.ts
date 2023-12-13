export interface Comment {
    _id: string,
    forename: string,
    surname: string,
    username: string
    profile_picture: string,
    text: string,
    date: string
}

export function remapComment(comment: Comment): Comment {
    const timeStamp = parseInt((comment._id).toString().substr(0,8), 16)*1000

    return {
        ...comment,
        date: new Date(timeStamp).toLocaleDateString('en-uk', { weekday:"long", year:"numeric", month:"short", day:"numeric"})
      };
}