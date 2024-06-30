
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name:'Index', component: () => import('pages/IndexPage.vue') },
      { path: 'lobby', name:'Lobby', component: () => import('pages/LobbyPage.vue')},
      { path: 'game', name:'Game', component: () => import('pages/GamePage.vue')},
      { path: 'sheet', name: 'Sheet', component: () => import('pages/CharacterSheet.vue')},
      { path: 'test', name: 'Test', component: () => import('pages/Test.vue')}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
