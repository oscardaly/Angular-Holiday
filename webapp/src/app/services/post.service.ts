import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';
import { HttpParamsBuilder } from '../HttpParamsBuilder';
import { remapComment } from '../post-card/comment';
import { Post, remapPost } from '../post-card/post';
import { Comment } from '../post-card/comment'

const BASEURL = "http://127.0.0.1:5000/api/v1.0/posts"
const baseHeaders = new HttpHeaders().set('content-type', 'content/json');

@Injectable({providedIn: 'root'})
export class PostService {
  private postsSubject = new BehaviorSubject<Post[]>([]);
  //can use this for caching entire array

  constructor(private http: HttpClient) {}

  createAuthorizationHeader(headers: Headers) {
    headers.append('x-access-token', ''); 
  }

  getPosts(): Observable<Post[]> {
    return this.postsSubject;
  }

  getPostsWithParams(params: GetPostsParams): Observable<Post[]> {
    const postParams = this.buildParams(params)

    return this.http
    .get<Post[]>(BASEURL, { headers: baseHeaders, params: postParams })
    .pipe(map(json => json.map(remapPost)));
  }

  getAllPosts(): Observable<Post[]> {
    return this.http
      .get<Post[]>(BASEURL, { headers: baseHeaders })
      .pipe(map(json => json.map(remapPost))
    );
  }

  refresh() {
    return this.getAllPosts()
        .subscribe(posts => this.postsSubject.next(posts));
  }

  clear(): void {
    this.postsSubject.next([]);
  }

  remove(postID: number): Observable<any> {
    return this.http.delete(BASEURL + "/" + postID)
      .pipe(
        tap(() => this.refresh())
    );
  }

  getPostByID(postID: string) {
    const params = new HttpParams().set('id', postID);

    return this.http.get<Post>(BASEURL + "/get-post", { headers: baseHeaders, params: params})
      .pipe(
        map(remapPost)
      );
  }

  getCommentsOnPost(postID: string, page: number, page_size: number, sort_by_direction: number): Observable<Comment[]> {
    const params = new HttpParams()
      .set('pn', page)
      .set('ps', page_size)
      .set('sort_direction', sort_by_direction);

    return this.http.get<Comment[]>(BASEURL + "/" + postID + "/comments", {headers: baseHeaders, params: params})
    .pipe(map(json => json.map(remapComment)));
  }

  addCommentToPost(text: string, postID: string) {
    console.log(BASEURL + "/" + postID + "/comments")
    return this.http.post(BASEURL + "/" + postID + "/comments", JSON.stringify({"text": text}), { headers: baseHeaders });
  }

  addPost(title: string, coverImage: string, description: string, text: string, cityID: number) {
    console.log("Done");
  }

  buildParams(params: GetPostsParams) {
    const builder = new HttpParamsBuilder();

    builder
      .append('pn', params.pn)
      .append('ps', params.ps)
      .append('sort_by_function', params.sort_by_function)
      .append('sort_by_direction', params.sort_by_direction);

    if (params.title) {
        builder.append('title', params.title);
    }

    if (params.city) {
      builder
        .append('city', params.city);
    }

    if (params.country) {
      builder
        .append('country', params.country);  
    }

    return builder.build();
  }
}

interface GetPostsParams {
  pn: number;
  ps: number; 
  sort_by_direction: number;
  sort_by_function: string;
  title?: string;
  city?: string;
  country?: string;
}
