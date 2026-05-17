import { View, Text } from '@tarojs/components'
import './index.scss'

export default function SchoolsPage() {
  return (
    <View className='schools-page'>
      <View className='schools-safe' />
      <Text className='schools-title'>学校列表</Text>
    </View>
  )
}
