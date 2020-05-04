# FSDN Development Manual

>   This file contains some requirements that developers should obey while developing FSDN.
>
>   Author: 聂希瑞

![](https://img.shields.io/badge/FSDN-Development_Manual-brightgreen.svg)![](https://img.shields.io/badge/Manual-Documentation-green.svg)

## Table of Contents

-   [Git & GitHub Requirements](#Git & GitHub Requirements)
    -   [1. Tips](# 1. Tips)
    -   [2. Operations](#2. Operations)
-   [API Requirements](#API Requirements)
-   [Documentation Requirements](#Documentation Requirements)
    -   [1. README](#1. README)
    -   [2. 需求文档](#2. 需求文档)
    -   [3. 设计文档](#3. 设计文档)



## Git & GitHub Requirements

### 1. Tips

-   **Take it seriously** 
    -   **DO NOT** commit or make a pull request to `master` branch casually！
-   **Explore on your own branch**
    -   Developers should only merge or commit their code to **`dev` branch or their own branch** on GitHub repository.
-   **Admin will check your pull request** 
    -   If you want to merge your code to `master` branch on GitHub repository, you can make a `pull request` from your own branch (or `dev` branch). **Let the admin decide whether to merge your branch into `master` branch or not.**
-   **Keep your commits clean** 
    -   If you want to push your code in local repository to remote repository,  **DO NOT** use `add .` command before `commit -m "blabla"` ! You should add your code and directories carefully! **DO NOT** add directories like `\venv` into your commit! It will cause many unnecessary code injecting to remote repository. 
-   **Update Kanban frequently and clearly**
    -   All teammates and group leaders should emphasize the importance of Kanban and use it in a efficient way. We can update our progress and targets clearly with Kanban.
    -   All contents in Kanban should be write in a clear format. When you add a TO-DO in Kanban, you should **write down the tasks, the deadlines, the person in charge clearly.**

### 2. Operations

To help you developing better, you may need to refer to operations below.

1.  create your local repository on your own PC.

    `git init`

2.  bind your local repository to remote repository. 

    `git remote add xxx`

3.  pull remote repository to local repository.

    `git pull origin dev/master`

4.  check out to your own branch.

    `git checkout dev`
    
5.  add your code to commits carefully.

    remember not to use` add .` command.

**Note:** The most important thing is that work in `dev` branch (or your own). Avoid committing your local code to wrong branch in remote repository.

## API Requirements

APIs are used to make a standard interface so that both backend and frontend developers can do their work clearly.  Read the [api.md](./api.md) for more details.

## Documentation Requirements

### 1. README

Both frontend and backend repository should have a README to introduce your repository. The README should be written in a standard way. See [README.md](./README.md) for more details.

### 2. 需求文档

### 3. 设计文档



