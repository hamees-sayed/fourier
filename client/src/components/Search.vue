<template>
    <form action="{{ url_for('song_search') }}" method="get" class="container input-group rounded w-50">
        <input type="search" name="q" class="form-control rounded border border-primary" placeholder="Search Songs" aria-label="Search"
            aria-describedby="search-addon" />
        <span class="input-group-text border-0" id="search-addon">
            <button type="submit" class="btn btn-link"><i class="fas fa-search"></i></button>
        </span>
    </form>
</template>