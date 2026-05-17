export default defineAppConfig({
  pages: [
    'pages/splash/index',
    'pages/home/index',
    'pages/schools/index',
    'pages/school-detail/index'
  ],
  window: {
    navigationStyle: 'custom',
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#ffffff',
    navigationBarTitleText: '青择校',
    navigationBarTextStyle: 'black',
    backgroundColor: '#ffffff'
  },
  lazyCodeLoading: 'requiredComponents',
  requiredPrivateInfos: []
})
