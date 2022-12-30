import { ScrollView, StyleSheet, Text, View } from 'react-native'
import React from 'react'
import { Button, Gap, Header, Input } from '../../components'
import { colors } from '../../utils'

const UpdateProfile = ({navigation}) => {
  return (
    <ScrollView>
      <Header title="Edit Profile" onPress={() => navigation.goBack()}/>
      <View style={styles.content}>
      <Input labelText="Full Name" />
      <Gap height={24} />
      <Input labelText="Pekerjaan" />
      <Gap height={24} />
      <Input labelText="Email" />
      <Gap height={24} />
      <Input labelText="Password" />
      <Gap height={40} />
      <Button title="Save Profile" />
    </View>
    </ScrollView>
  )
}

export default UpdateProfile

const styles = StyleSheet.create({
    content:{
        color: "yellow",
        flex: 1,
    }
})