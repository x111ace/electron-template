<script lang="ts">
    // @ts-nocheck
    export let params = {};
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import './styles/entry-page.css';

    onMount(() => {
        const enterButton = document.getElementById('enterMainPage');
        if (enterButton) {
            enterButton.addEventListener('click', async () => {
                if (window.electronAPI) {
                    window.electronAPI.send('notify', 'User has entered the game page.');
                }
                await goto('/game');
            });
        }
    });
</script>

<div class="entry-page-container">
    <h1>Hello, World!</h1>
    <button id="enterMainPage" class="centered-button">Enter the Main Page</button>
</div> 