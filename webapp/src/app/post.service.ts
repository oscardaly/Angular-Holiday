import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap, map } from 'rxjs/operators';
import { Post, remapPost } from './post-card/post';

const BASEURL = "http://127.0.0.1:5000/api/v1.0/posts"
const baseHeaders = new HttpHeaders().set('content-type', 'content/json');

@Injectable({providedIn: 'root'})
export class PostService {
  private postsSubject = new BehaviorSubject<Post[]>([]);

  constructor(private http: HttpClient) {}

  createAuthorizationHeader(headers: Headers) {
    headers.append('x-access-token', ''); 
  }

  getPosts(): Observable<Post[]> {
    return this.postsSubject;
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

    return this.http.get<Post>(BASEURL + "/get-post?id=" + postID, { headers: baseHeaders, params: params})
      .pipe(
          map(remapPost)
        );
    }

  addPost(title: string, coverImage: string, description: string, text: string, cityID: number) {
    console.log("Done");
  }
}
