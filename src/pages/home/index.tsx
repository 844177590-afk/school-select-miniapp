import { View, Text } from '@tarojs/components'
import './index.scss'

export default function HomePage() {
  return (
    <View className='home-page'>
      <View className='home-safe' />
      <View className='home-main'>
        <Text className='home-title'>搜学校 搜专业</Text>
        <View className='home-search'>
          <Text className='home-placeholder'>输入学校或专业</Text>
          <View className='home-search-action'>搜</View>
        </View>
        <View className='home-tags'>
          {['护理', '铁路', '计算机', '西安', '公办'].map((item) => (
            <Text className='home-tag' key={item}>
              {item}
            </Text>
          ))}
        </View>
      </View>
    </View>
  )
}
