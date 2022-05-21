import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup  } from '../../components'
import MetaTags from 'react-meta-tags'
import styles from "./styles.module.css"

const Shop = () => {
    return (
        <Main>
            <Container>
                <MetaTags>
                <title>Магазин</title>
                </MetaTags>

                <div className={styles.title}>
                    <Title title='Магазин' />
                    
                </div>

            </Container>
        </Main>
    )
}


export default Shop