import { Comment } from "./comment"

export interface Post {
    _id: string,
    author: {
        forename: string,
        surname: string,
        username: string,
        profile_picture: string
    },
    city: {
        city: string,
        city_ascii: string,
        country: string,
        population: string,
        lat: number,
        lng: number,
        id: string
    }
    text: string,
    cover_photo: string,
    title: string,
    description: string,
    comments: Comment[]
    date: string
}

export function remapPost(post: Post): Post {
    const timeStamp = parseInt((post._id).toString().substr(0,8), 16)*1000

    return {
        ...post,
        date: new Date(timeStamp).toLocaleDateString('en-uk', { weekday:"long", year:"numeric", month:"short", day:"numeric"})
      };
}
