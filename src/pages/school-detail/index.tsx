import { View, Text } from '@tarojs/components'
import './index.scss'

export default function SchoolDetailPage() {
  return (
    <View className='detail-page'>
      <View className='detail-gallery' />
      <Text className='detail-title'>学校详情</Text>
    </View>
  )
}
